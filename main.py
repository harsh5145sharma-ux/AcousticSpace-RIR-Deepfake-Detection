import logging
import os
import numpy as np
from src.utils import audio_to_spectrogram
from src.data_loader import get_audio_paths
from models.inference import predict

# Configure logging to track progress for the team
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_batch_processing(csv_file):
    paths = get_audio_paths(csv_file)
    logging.info(f"Starting batch for {len(paths)} files.")
    
    # Ensure processed directory exists
    if not os.path.exists("processed"):
        os.makedirs("processed")
    
    for path in paths:
        try:
            spec = audio_to_spectrogram(path)
            file_name = os.path.basename(path).replace(".wav", ".npy")
            save_path = os.path.join("processed", file_name)
            np.save(save_path, spec)
        
            result = predict(spec)
            
            logging.info(f"Saved {file_name}. Processed: {result}")

        except Exception as e:
            logging.error(f"Failed to process {path}: {e}")

if __name__ == "__main__":
    run_batch_processing("metadata.csv")