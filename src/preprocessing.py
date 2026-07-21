import librosa
import numpy as np
import pandas as pd
import os
import json

# Repo-relative base paths (no more hardcoded /workspace/... paths).
# SRC_DIR = .../repo/src, ROOT_DIR = .../repo
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)

DEFAULT_METADATA_PATH = os.path.join(ROOT_DIR, "metadata.csv")
DEFAULT_AUDIO_ROOT = os.path.join(ROOT_DIR, "BEFORE_TRAIN")
DEFAULT_OUTPUT_DIR = os.path.join(ROOT_DIR, "output")


def extract_rir_features(audio_path):
    """
    Dummy RIR feature extraction.
    Placeholder for actual RIR logic.
    """
    y, sr = librosa.load(audio_path, sr=None)
    # Placeholder: MFCCs as a proxy for RIR features for pipeline testing
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs, axis=1)


def resolve_audio_path(row, audio_root):
    """
    Build the local audio path for a metadata row using the repo's
    BEFORE_TRAIN/<label>/<filename> layout, instead of relying on the
    absolute before_path stored in metadata.csv (which points to a
    Colab-only location).
    """
    return os.path.join(audio_root, row["label"], row["filename"])


def process_dataset(metadata_path=DEFAULT_METADATA_PATH,
                     audio_root=DEFAULT_AUDIO_ROOT,
                     output_dir=DEFAULT_OUTPUT_DIR):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(metadata_path)
    features = []

    for _, row in df.iterrows():
        audio_path = resolve_audio_path(row, audio_root)

        # NOTE: This assumes files are available locally under BEFORE_TRAIN/.
        try:
            feats = extract_rir_features(audio_path)
            features.append({
                "filename": row["filename"],
                "label": row["label"],
                "features": feats.tolist()
            })
        except Exception as e:
            print(f"Error processing {audio_path}: {e}")

    with open(os.path.join(output_dir, "dataset_features.json"), "w") as f:
        json.dump(features, f)


if __name__ == "__main__":
    process_dataset()
