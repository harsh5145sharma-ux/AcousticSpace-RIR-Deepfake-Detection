from src.utils import audio_to_spectrogram
from src.data_loader import get_audio_paths
import os

def run_batch_processing(csv_file):
    filenames = get_audio_paths(csv_file)
    for name in filenames:
        print(f"Processing {name}...")
        # Add logic to call audio_to_spectrogram here
        
if __name__ == "__main__":
    run_batch_processing("metadata.csv")