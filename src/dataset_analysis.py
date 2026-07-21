import librosa
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import os

# Repo-relative base paths (no more hardcoded /workspace/... paths).
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)

DEFAULT_METADATA_PATH = os.path.join(ROOT_DIR, "metadata.csv")
DEFAULT_OUTPUT_DIR = os.path.join(ROOT_DIR, "output")


def plot_spectrogram(audio_path, output_path):
    y, sr = librosa.load(audio_path, sr=None)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def analyze_dataset(metadata_path):
    df = pd.read_csv(metadata_path)
    report = {
        "total_samples": len(df),
        "class_distribution": df['label'].value_counts().to_dict(),
        "split_distribution": df['split'].value_counts().to_dict(),
        "average_duration": df['duration'].mean()
    }
    return report

if __name__ == "__main__":
    os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
    report = analyze_dataset(DEFAULT_METADATA_PATH)

    report_path = os.path.join(DEFAULT_OUTPUT_DIR, "dataset_analysis_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"Analysis complete. Report generated at {report_path}")
