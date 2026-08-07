"""
preprocessing.py
=================
AcousticSpace — Deepfake Detection via Room Impulse Response (RIR)
Member 1: ML / Audio Pipeline

Purpose
-------
This module is the single entry point for turning raw audio files
(ASVspoof-style bonafide/spoof recordings) into a clean, model-ready
feature set. It handles:

    1. Audio loading & normalization
    2. RIR-related acoustic feature extraction
       (RT60 estimate, spectral features, MFCCs, energy decay curve)
    3. Dataset curation / cleaning (corrupt file detection, resampling,
       silence trimming)
    4. Batch processing over an ASVspoof protocol file into a single
       feature table (CSV/Parquet) that Member 2 (AST model) consumes
       directly.

Usage
-----
    python preprocessing.py --protocol data/raw/protocol.txt \
                             --audio_dir data/raw/wav \
                             --out data/processed/features.csv

Output feature table columns:
    file_id, label, rt60, edt, c50, spectral_centroid_mean,
    spectral_bandwidth_mean, spectral_rolloff_mean, zcr_mean,
    mfcc_1 ... mfcc_13, rms_mean, duration_sec
"""

from __future__ import annotations

import argparse
import logging
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import librosa
import soundfile as sf

# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #

SAMPLE_RATE = 16000          # ASVspoof standard sample rate
N_MFCC = 13
FRAME_LENGTH = 2048
HOP_LENGTH = 512
MIN_DURATION_SEC = 0.3        # files shorter than this are dropped as corrupt/junk

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("acousticspace.preprocessing")


# --------------------------------------------------------------------------- #
# Data classes
# --------------------------------------------------------------------------- #

@dataclass
class RIRFeatures:
    """Container for one audio file's extracted feature vector."""
    file_id: str
    label: str
    rt60: float
    edt: float
    c50: float
    spectral_centroid_mean: float
    spectral_bandwidth_mean: float
    spectral_rolloff_mean: float
    zcr_mean: float
    rms_mean: float
    duration_sec: float
    mfcc: np.ndarray  # shape (N_MFCC,)

    def to_row(self) -> dict:
        row = asdict(self)
        mfcc = row.pop("mfcc")
        for i, v in enumerate(mfcc, start=1):
            row[f"mfcc_{i}"] = float(v)
        return row


# --------------------------------------------------------------------------- #
# Loading & cleaning
# --------------------------------------------------------------------------- #

def load_audio(path: str, sr: int = SAMPLE_RATE) -> Optional[np.ndarray]:
    """
    Load an audio file, resample to `sr`, convert to mono, and trim
    leading/trailing silence. Returns None if the file is corrupt,
    unreadable, or too short to be usable (logged, not raised, so a
    batch job doesn't die on one bad file).
    """
    try:
        y, orig_sr = sf.read(path, always_2d=False)
    except Exception as e:
        logger.warning(f"Could not read {path}: {e}")
        return None

    if y.ndim > 1:
        y = np.mean(y, axis=1)  # downmix to mono

    if orig_sr != sr:
        y = librosa.resample(y.astype(np.float32), orig_sr=orig_sr, target_sr=sr)

    y, _ = librosa.effects.trim(y, top_db=30)

    if len(y) / sr < MIN_DURATION_SEC:
        logger.warning(f"Skipping {path}: too short after trimming ({len(y)/sr:.3f}s)")
        return None

    # peak normalize to avoid clipping artifacts skewing spectral features
    peak = np.max(np.abs(y)) + 1e-9
    y = y / peak

    return y


# --------------------------------------------------------------------------- #
# RIR-specific feature extraction
# --------------------------------------------------------------------------- #

def estimate_energy_decay_curve(y: np.ndarray) -> np.ndarray:
    """
    Schroeder backward integration: converts the (squared) signal into
    an energy decay curve, which RT60/EDT/C50 are derived from. This is
    the standard method used in room-acoustics analysis and is what
    makes these features informative for RIR-based spoof detection —
    synthetic speech tends to carry an unnatural or absent reverberant
    tail compared to genuine room recordings.
    """
    energy = y[::-1] ** 2
    edc = np.cumsum(energy)[::-1]
    edc = edc / (np.max(edc) + 1e-12)
    edc_db = 10 * np.log10(edc + 1e-12)
    return edc_db


def estimate_rt60(edc_db: np.ndarray, sr: int = SAMPLE_RATE) -> float:
    """
    Estimate RT60 (time for sound to decay 60dB) using a T20 extrapolation
    (measuring the -5dB to -25dB slope and extrapolating to -60dB), which
    is more robust to noise floor issues than measuring the full 60dB span
    directly on short speech clips.
    """
    try:
        idx_start = np.where(edc_db <= -5)[0][0]
        idx_end = np.where(edc_db <= -25)[0][0]
    except IndexError:
        return 0.0

    if idx_end <= idx_start:
        return 0.0

    t_start, t_end = idx_start / sr, idx_end / sr
    slope = (edc_db[idx_end] - edc_db[idx_start]) / (t_end - t_start + 1e-9)
    if slope == 0:
        return 0.0
    rt60 = -60.0 / slope
    return float(np.clip(rt60, 0, 3.0))  # clip to plausible room range


def estimate_edt(edc_db: np.ndarray, sr: int = SAMPLE_RATE) -> float:
    """Early Decay Time: slope from 0dB to -10dB, extrapolated to -60dB."""
    try:
        idx_end = np.where(edc_db <= -10)[0][0]
    except IndexError:
        return 0.0
    if idx_end == 0:
        return 0.0
    t_end = idx_end / sr
    slope = (edc_db[idx_end] - edc_db[0]) / t_end
    if slope == 0:
        return 0.0
    edt = -60.0 / slope
    return float(np.clip(edt, 0, 3.0))


def estimate_c50(y: np.ndarray, sr: int = SAMPLE_RATE) -> float:
    """
    Clarity index C50: ratio (in dB) of early energy (0-50ms) to late
    energy (>50ms). Low/absent-reverb synthetic audio tends to produce
    anomalously high C50 values.
    """
    split = int(0.05 * sr)
    early = np.sum(y[:split] ** 2)
    late = np.sum(y[split:] ** 2)
    if late <= 0:
        return 0.0
    c50 = 10 * np.log10((early + 1e-12) / (late + 1e-12))
    return float(c50)


def extract_features(y: np.ndarray, file_id: str, label: str, sr: int = SAMPLE_RATE) -> RIRFeatures:
    """Extract the full RIR + spectral feature vector for one audio clip."""
    edc_db = estimate_energy_decay_curve(y)
    rt60 = estimate_rt60(edc_db, sr)
    edt = estimate_edt(edc_db, sr)
    c50 = estimate_c50(y, sr)

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=HOP_LENGTH)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr, hop_length=HOP_LENGTH)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, hop_length=HOP_LENGTH)
    zcr = librosa.feature.zero_crossing_rate(y, hop_length=HOP_LENGTH)
    rms = librosa.feature.rms(y=y, hop_length=HOP_LENGTH)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=N_MFCC, hop_length=HOP_LENGTH)

    return RIRFeatures(
        file_id=file_id,
        label=label,
        rt60=rt60,
        edt=edt,
        c50=c50,
        spectral_centroid_mean=float(np.mean(spectral_centroid)),
        spectral_bandwidth_mean=float(np.mean(spectral_bandwidth)),
        spectral_rolloff_mean=float(np.mean(spectral_rolloff)),
        zcr_mean=float(np.mean(zcr)),
        rms_mean=float(np.mean(rms)),
        duration_sec=float(len(y) / sr),
        mfcc=np.mean(mfcc, axis=1),
    )
# --------------------------------------------------------------------------- #
# Single-audio inference preprocessing
# --------------------------------------------------------------------------- #

def preprocess_audio(file_path: str) -> np.ndarray:
    """
    Preprocess a single uploaded audio file for backend/model inference.

    Parameters
    ----------
    file_path : str
        Path to an audio file (.wav, .flac, .mp3).

    Returns
    -------
    np.ndarray
        Feature vector with:
        shape = (22,)
        dtype = float32

    Processing:
        1. Load audio
        2. Convert to mono
        3. Resample to SAMPLE_RATE (16 kHz)
        4. Trim silence
        5. Peak normalize
        6. Extract RIR/acoustic features
        7. Extract spectral features
        8. Extract MFCC features
    """

    # ---------------------------
    # Validate input path
    # ---------------------------

    if not isinstance(file_path, (str, os.PathLike)):
        raise TypeError(
            "file_path must be a string or path-like object"
        )

    file_path = str(file_path)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"Audio file not found: {file_path}"
        )

    # ---------------------------
    # Validate audio extension
    # ---------------------------

    extension = Path(file_path).suffix.lower()

    supported_extensions = {
        ".wav",
        ".flac",
        ".mp3",
    }

    if extension not in supported_extensions:
        raise ValueError(
            f"Unsupported audio format: {extension}. "
            "Supported formats: WAV, FLAC, MP3"
        )

    # ---------------------------
    # Existing Member 1 pipeline
    # ---------------------------

    y = load_audio(
        file_path,
        sr=SAMPLE_RATE,
    )

    if y is None:
        raise ValueError(
            "Audio preprocessing failed. "
            "The audio may be corrupt, silent, unreadable "
            "or shorter than the minimum duration."
        )

    # ---------------------------
    # Existing feature extraction
    # ---------------------------

    features = extract_features(
        y=y,
        file_id=Path(file_path).stem,
        label="unknown",
        sr=SAMPLE_RATE,
    )

    # ---------------------------
    # Convert features to fixed
    # model-ready NumPy vector
    # ---------------------------

    feature_vector = np.array(
        [
            features.rt60,
            features.edt,
            features.c50,
            features.spectral_centroid_mean,
            features.spectral_bandwidth_mean,
            features.spectral_rolloff_mean,
            features.zcr_mean,
            features.rms_mean,
            features.duration_sec,
            *features.mfcc.tolist(),
        ],
        dtype=np.float32,
    )

    # ---------------------------
    # Validate output
    # ---------------------------

    if feature_vector.shape != (22,):
        raise RuntimeError(
            "Unexpected preprocessing output shape. "
            f"Expected (22,), got {feature_vector.shape}"
        )

    if not np.all(np.isfinite(feature_vector)):
        raise ValueError(
            "Preprocessing generated NaN or infinite values"
        )

    return feature_vector

# --------------------------------------------------------------------------- #
# Batch pipeline
# --------------------------------------------------------------------------- #

def read_protocol(protocol_path: str) -> pd.DataFrame:
    """
    Reads an ASVspoof-style protocol file. Expected whitespace-separated
    columns: speaker_id file_id system_id label(bonafide/spoof) [...].
    Adjust `col_names` below if your protocol variant differs.
    """
    col_names = ["speaker_id", "file_id", "system_id", "unused", "label"]
    df = pd.read_csv(protocol_path, sep=r"\s+", header=None, names=col_names)
    return df[["file_id", "label"]]


def read_protocol_csv(protocol_path: str) -> pd.DataFrame:
    """
    Reads a simple 2-column CSV protocol: file_id,label
    (no header, or a header named file_id/label — both are handled).
    This is the format produced by `build_protocol_from_prefix()` below,
    and the simplest format to hand-write for a small custom dataset.
    """
    df = pd.read_csv(protocol_path)
    if not {"file_id", "label"}.issubset(df.columns):
        # assume headerless two-column csv
        df = pd.read_csv(protocol_path, header=None, names=["file_id", "label"])
    return df[["file_id", "label"]]


def build_protocol_from_prefix(
    audio_dir: str,
    ext: str = ".wav",
    label_map: Optional[dict] = None,
    out_path: Optional[str] = None,
) -> pd.DataFrame:
    """
    Auto-generates a protocol table by reading the filename prefix of every
    audio file in `audio_dir` — useful for small custom datasets like
    `ai_001.wav`, `ai_002.wav`, `real_001.wav`, ... where the label is
    already encoded in the filename and a separate protocol file would be
    redundant.

    label_map maps filename-prefix -> label string, e.g.:
        {"ai": "spoof", "real": "bonafide"}
    Any filename whose prefix isn't in label_map is skipped (logged).

    If `out_path` is given, the resulting table is also saved as CSV so it
    can be reused as a protocol file for later runs / other members.
    """
    if label_map is None:
        label_map = {"ai": "spoof", "real": "bonafide"}

    rows = []
    skipped = []
    for fname in sorted(os.listdir(audio_dir)):
        if not fname.lower().endswith(ext.lower()):
            continue
        stem = os.path.splitext(fname)[0]
        prefix = stem.split("_")[0].lower()

        if prefix not in label_map:
            skipped.append(fname)
            continue

        rows.append({"file_id": stem, "label": label_map[prefix]})

    if skipped:
        logger.warning(
            f"{len(skipped)} file(s) had an unrecognized prefix and were skipped: "
            f"{skipped[:5]}{'...' if len(skipped) > 5 else ''}"
        )

    df = pd.DataFrame(rows)
    counts = df["label"].value_counts().to_dict() if len(df) else {}
    logger.info(f"Built protocol from filenames: {len(df)} files. Class counts: {counts}")

    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_path, index=False)
        logger.info(f"Saved auto-generated protocol to {out_path}")

    return df


def build_feature_table(
    protocol_path: Optional[str],
    audio_dir: str,
    ext: str = ".flac",
    protocol_format: str = "asvspoof",
    label_map: Optional[dict] = None,
) -> pd.DataFrame:
    """
    Runs the full pipeline over every file in the protocol and returns a DataFrame.

    protocol_format:
        "asvspoof" — whitespace-separated ASVspoof protocol file (default)
        "csv"      — simple file_id,label CSV (see read_protocol_csv)
        "prefix"   — no protocol file needed; labels are inferred from
                     filename prefixes in `audio_dir` (see build_protocol_from_prefix)
    """
    if protocol_format == "asvspoof":
        protocol_df = read_protocol(protocol_path)
    elif protocol_format == "csv":
        protocol_df = read_protocol_csv(protocol_path)
    elif protocol_format == "prefix":
        protocol_df = build_protocol_from_prefix(audio_dir, ext=ext, label_map=label_map)
    else:
        raise ValueError(f"Unknown protocol_format: {protocol_format}")

    rows = []
    n_skipped = 0

    for _, row in protocol_df.iterrows():
        file_id, label = row["file_id"], row["label"]
        audio_path = os.path.join(audio_dir, f"{file_id}{ext}")

        if not os.path.exists(audio_path):
            logger.warning(f"Missing audio file: {audio_path}")
            n_skipped += 1
            continue

        y = load_audio(audio_path)
        if y is None:
            n_skipped += 1
            continue

        feats = extract_features(y, file_id, label)
        rows.append(feats.to_row())

    logger.info(f"Processed {len(rows)} files, skipped {n_skipped} (missing/corrupt/too short).")
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# CLI entry point
# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(description="AcousticSpace RIR feature extraction pipeline")
    parser.add_argument(
        "--protocol",
        default=None,
        help="Path to protocol file (ASVspoof .txt or file_id,label .csv). "
             "Not needed if --protocol_format prefix is used.",
    )
    parser.add_argument("--audio_dir", required=True, help="Directory containing audio files")
    parser.add_argument("--ext", default=".flac", help="Audio file extension (default: .flac)")
    parser.add_argument("--out", default="data/processed/features.csv", help="Output CSV path")
    parser.add_argument(
        "--protocol_format",
        choices=["asvspoof", "csv", "prefix"],
        default="asvspoof",
        help="'asvspoof' = protocol .txt file (default); 'csv' = simple file_id,label csv; "
             "'prefix' = infer labels from filename prefixes (e.g. ai_001.wav, real_001.wav), "
             "no protocol file needed.",
    )
    parser.add_argument(
        "--label_map",
        default="ai:spoof,real:bonafide",
        help="Only used with --protocol_format prefix. Comma-separated prefix:label pairs, "
             "e.g. 'ai:spoof,real:bonafide,fake:spoof'.",
    )
    args = parser.parse_args()

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    label_map = None
    if args.protocol_format == "prefix":
        label_map = dict(pair.split(":") for pair in args.label_map.split(","))

    if args.protocol_format != "prefix" and not args.protocol:
        parser.error("--protocol is required unless --protocol_format prefix is used")

    df = build_feature_table(
        args.protocol,
        args.audio_dir,
        args.ext,
        protocol_format=args.protocol_format,
        label_map=label_map,
    )
    df.to_csv(args.out, index=False)
    logger.info(f"Saved feature table with {len(df)} rows to {args.out}")


if __name__ == "__main__":
    main()
