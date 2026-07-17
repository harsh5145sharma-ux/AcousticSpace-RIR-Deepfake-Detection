import librosa
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import os

# Set dummy audio paths for demo
AUDIO_DIR = "/workspace/inputs"

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
    metadata_path = "/workspace/inputs/metadata-4543.csv"
    report = analyze_dataset(metadata_path)
    
    with open("/workspace/member1_work/dataset_analysis_report.json", 'w') as f:
        json.dump(report, f, indent=4)
        
    print("Analysis complete. Report generated.")
