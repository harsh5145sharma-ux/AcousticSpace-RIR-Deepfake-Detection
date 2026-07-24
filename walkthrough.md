# Workspace Execution Summary — AcousticSpace Audio Pipeline

Here is the complete overview of the executed files, test results, and generated artifacts in your workspace: **`c:\acoustic space2`**.

---

## 📁 Workspace Directory Structure

```
c:\acoustic space2\
├── README.md                                    # Project documentation
├── preprocessing.py                             # Core audio preprocessing & feature extraction script
└── acousticspace-audio-pipeline/
    ├── data/
    │   ├── Dataset/                             # 172 raw audio files (.wav)
    │   └── processed/
    │       └── features.csv                     # ✨ Output CSV (172 rows of extracted features)
    ├── notebooks/
    │   └── feature_extraction.ipynb             # Interactive analysis notebook
    ├── reports/
    │   └── dataset_analysis_report.md           # Dataset statistics & feature rationale
    └── tests/
        └── test_preprocessing.py                # Unit test suite (8 tests passed)
```

---

## 📄 Key File Links

- **Main Processing Script**: [preprocessing.py](file:///c:/acoustic%20space2/preprocessing.py)
- **Extracted Features Table**: [features.csv](file:///c:/acoustic%20space2/acousticspace-audio-pipeline/data/processed/features.csv)
- **Unit Tests**: [test_preprocessing.py](file:///c:/acoustic%20space2/acousticspace-audio-pipeline/tests/test_preprocessing.py)
- **Analysis Notebook**: [feature_extraction.ipynb](file:///c:/acoustic%20space2/acousticspace-audio-pipeline/notebooks/feature_extraction.ipynb)
- **Dataset Report**: [dataset_analysis_report.md](file:///c:/acoustic%20space2/acousticspace-audio-pipeline/reports/dataset_analysis_report.md)
- **Project README**: [README.md](file:///c:/acoustic%20space2/README.md)

---

## 🧪 Execution & Verification Summary

### 1. Unit Tests (`pytest tests/`)
- **Status**: ✅ **8 / 8 Passed**
- Covered functions: `load_audio`, `estimate_energy_decay_curve`, `estimate_rt60`, `estimate_edt`, `estimate_c50`, `extract_features`.

### 2. Feature Extraction Run (`preprocessing.py`)
- **Input**: 172 audio clips from `data/Dataset` (100 AI spoof, 72 human bonafide)
- **Output**: [features.csv](file:///c:/acoustic%20space2/acousticspace-audio-pipeline/data/processed/features.csv) containing 172 feature rows with:
  - **Room Impulse Response (RIR)**: RT60, EDT, C50
  - **Spectral Attributes**: Spectral Centroid, Bandwidth, Rolloff, Zero-Crossing Rate, RMS Energy
  - **MFCCs**: 13 coefficients (`mfcc_1` to `mfcc_13`)
