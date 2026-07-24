# AcousticSpace — Audio Pipeline (Member 1)

Deepfake detection via Room Impulse Response (RIR) features — this repo contains
the audio preprocessing and feature extraction pipeline that feeds Member 2's
AST classifier.

## What's in here

```
acousticspace-audio-pipeline/
├── preprocessing.py                    # Core pipeline: load, clean, extract features, batch-run
├── notebooks/
│   └── feature_extraction.ipynb        # Interactive walkthrough with plots
├── reports/
│   └── dataset_analysis_report.md      # Dataset stats, quality checks, feature rationale
├── data/
│   ├── raw/                            # Raw ASVspoof audio + protocol file (gitignored)
│   └── processed/                      # Output feature tables (gitignored)
├── tests/
│   └── test_preprocessing.py           # Unit tests for feature extraction
├── requirements.txt
└── .gitignore
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. Drop the ASVspoof protocol file and audio into `data/raw/`.
2. Run the pipeline:

```bash
python preprocessing.py \
    --protocol data/raw/protocol.txt \
    --audio_dir data/raw/wav \
    --ext .flac \
    --out data/processed/features.csv
```

3. Or explore interactively:

```bash
jupyter notebook notebooks/feature_extraction.ipynb
```

The output `features.csv` is what Member 2 consumes for AST fine-tuning — schema
is documented in the `preprocessing.py` module docstring and in
`reports/dataset_analysis_report.md`.

## Features extracted

RT60, EDT, C50 (room-acoustics / RIR features) + spectral centroid/bandwidth/rolloff,
zero-crossing rate, RMS energy, and 13 MFCC coefficients. Rationale for each is in
the dataset analysis report.

## Running tests

```bash
pytest tests/
```

## Branch

Work happens on `feature/audio-pipeline`, merged into `develop` at the weekly
Friday integration checkpoint. See the team's root `CONTRIBUTING.md` / work
distribution doc for the full git workflow and commit message conventions.

## Dependencies on other members

- **Blocks Member 2**: AST model training reads `data/processed/features.csv`
  produced here — flag early if the feature schema needs to change.
- **Needs**: dataset access confirmed ASAP (see open questions in the dataset
  analysis report).
