# AcousticSpace — Audio Pipeline (Member 1)

**Role:** ML / Audio Pipeline Lead
**Layer:** `[Audio Data] → [Feature Extraction]` → (feeds into Member 2's AI model)

## Overview

This module is the foundation layer of AcousticSpace, a deepfake audio detector that works by analyzing **Room Impulse Response (RIR)** instead of voice tone/pitch. Traditional detectors check voice artifacts, which modern AI easily fools. AcousticSpace instead checks whether the room acoustics (echo, reverb) embedded in an audio clip actually match the environment it claims to be recorded in — a mismatch signals a fake.

This directory handles everything **before** the model sees the data:
1. Loading and labeling the raw dataset (ASVspoof)
2. Preprocessing raw audio
3. Extracting RIR-related features and spectrograms
4. Saving them in a format Member 2's AST (Audio Spectrogram Transformer) model can consume directly

---

## Folder Structure

```
member1-branch/
├── data/
│   ├── raw/                # original ASVspoof audio files (not committed — see .gitignore)
│   └── processed/          # extracted features, saved as .npy / .pt (not committed)
├── notebooks/
│   └── exploration.ipynb   # EDA, feature experiments, sample visualizations
├── src/
│   ├── data_loader.py      # loads ASVspoof file paths + bonafide/spoof labels
│   ├── preprocessing.py    # resampling, mono conversion, silence trimming, normalization
│   ├── spectrogram.py      # mel-spectrogram / log-spectrogram extraction
│   ├── rir_extraction.py   # RIR estimation + RT60 (reverberation time) features
│   └── feature_pipeline.py # orchestrates the full pipeline end-to-end
├── tests/
│   └── test_pipeline.py    # sanity checks for loader + preprocessing + feature shapes
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# clone and switch to this branch
git clone https://github.com/harsh5145sharma-ux/AcousticSpace-RIR-Deepfake-Detection.git
cd AcousticSpace-RIR-Deepfake-Detection
git checkout member1-branch

# create environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

### requirements.txt (core)
```
librosa
numpy
scipy
soundfile
torch
torchaudio
matplotlib
```

---

## Dataset

Uses **ASVspoof** — contains `bonafide` (real) and `spoof` (fake/synthetic) audio samples.

Expected raw layout:
```
data/raw/
├── bonafide/
│   ├── sample_0001.wav
│   └── ...
├── spoof/
│   ├── sample_0001.wav
│   └── ...
└── labels.csv        # filename, label, (optional) claimed_environment
```

Run the loader to verify the dataset is correctly indexed:
```bash
python src/data_loader.py
```

---

## Pipeline Steps

### 1. Preprocessing (`preprocessing.py`)
- Convert to mono
- Resample to a fixed sample rate (e.g. 16 kHz)
- Trim leading/trailing silence
- Normalize amplitude

### 2. Spectrogram Extraction (`spectrogram.py`)
- Computes log-mel spectrogram per clip (input format expected by AST models)
- Configurable: n_mels, hop_length, win_length

### 3. RIR / Reverb Feature Extraction (`rir_extraction.py`)
- Estimates the Room Impulse Response from the recording (blind estimation / deconvolution-based)
- Extracts RT60 (reverberation decay time) and related acoustic descriptors
- These are the features that let the model tell if the "room" in the audio is real or inconsistent

### 4. Full Pipeline (`feature_pipeline.py`)
Runs preprocessing → spectrogram → RIR extraction → saves output.

```bash
python src/feature_pipeline.py --input data/raw --output data/processed
```

---

## Output Format (for Member 2)

Each processed sample is saved as a `.pt` (or `.npy`) file containing:

```python
{
  "spectrogram": Tensor[shape=(n_mels, time_frames)],
  "rir_features": Tensor[shape=(n_rir_features,)],
  "label": int,          # 0 = bonafide, 1 = spoof
  "filename": str
}
```

All processed files are indexed in `data/processed/manifest.csv`:

```
filename, feature_path, label
sample_0001.wav, data/processed/sample_0001.pt, 0
```

**Member 2 should load features via `manifest.csv`** — this keeps the pipeline decoupled from the training code.

---

## Running Tests

```bash
pytest tests/
```

Covers:
- Dataset loads with correct label counts
- Preprocessing handles edge cases (silence-only clips, very short clips, mismatched sample rates)
- Feature output shapes are consistent across samples

---

## For Member 2 (Model Engineer)
- A small sample feature set (~10-20 processed files) is available early in `data/processed/sample_subset/` so you can start building the training loop without waiting on the full pipeline.
- Feature shapes and the manifest format above won't change without a note here — flag me if you need a different format.

## Status / Progress
- [x] Dataset loader
- [x] Preprocessing
- [x] Spectrogram extraction
- [ ] RIR estimation (in progress)
- [ ] RT60 feature extraction
- [ ] Full pipeline integration
- [ ] Unit tests

---

## Notes
- Raw audio and large processed files are gitignored — only code, configs, and small sample subsets are committed.
- Merges into `develop` happen every Friday per team convention.
