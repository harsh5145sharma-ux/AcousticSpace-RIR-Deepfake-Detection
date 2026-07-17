# Audio Pipeline - Member 1

This repository contains the audio preprocessing and RIR feature extraction pipeline for the "Deepfake Detection via Room Impulse Response" project.

## Project Structure
- `src/preprocessing.py`: Core Librosa pipeline for feature extraction.
- `src/dataset_analysis.py`: Dataset exploration and statistical analysis.
- `dataset_analysis_report.json`: Output of the initial dataset metadata analysis.

## Setup Instructions
1. Install requirements: `pip install librosa pandas matplotlib numpy`
2. Run preprocessing: `python src/preprocessing.py`
3. Run analysis: `python src/dataset_analysis.py`

## Features
- RIR feature extraction proxy (MFCCs).
- Comprehensive dataset label and split statistics.
