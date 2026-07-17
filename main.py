from src.utils import audio_to_spectrogram
from src.data_loader import get_audio_paths
from models.inference import predict  # Import the mock inference
import os

def run_batch_processing(csv_file):
    print(f"Loading data from {csv_file}...")
    paths = get_audio_paths(csv_file)
    
    for path in paths:
        if os.path.exists(path):
            print(f"Processing: {path}")
            # 1. Get features
            spec = audio_to_spectrogram(path)
            
            # 2. Get prediction from mock model
            result = predict(spec)
            
            # 3. Output the result
            print(f"Result for {os.path.basename(path)}: {result}")
        else:
            print(f"Warning: File not found at {path}")

if __name__ == "__main__":
    run_batch_processing("metadata.csv")