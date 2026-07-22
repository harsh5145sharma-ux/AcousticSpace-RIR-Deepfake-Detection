import os
import numpy as np
from src.data_loader import get_audio_paths
from src.utils import audio_to_spectrogram
from config import DATA_DIR, PROCESSED_DIR, METADATA_FILE

def run_pipeline():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    paths = get_audio_paths(METADATA_FILE)
    print(f"Starting batch processing for {len(paths)} audio files...")
    
    for audio_path in paths:
        if os.path.exists(audio_path):
            spec = audio_to_spectrogram(audio_path)
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            output_path = os.path.join(PROCESSED_DIR, f"{base_name}.npy")
            np.save(output_path, spec)
            print(f"Processed and saved: {output_path}")
        else:
            print(f"Warning: File not found -> {audio_path}")

if __name__ == "__main__":
    run_pipeline()