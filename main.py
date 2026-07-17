import logging
from src.utils import audio_to_spectrogram
from src.data_loader import get_audio_paths
from models.inference import predict
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_batch_processing(csv_file):
    paths = get_audio_paths(csv_file)
    logging.info(f"Starting batch for {len(paths)} files.")
    
    for path in paths:
        try:
            spec = audio_to_spectrogram(path)
            result = predict(spec)
            logging.info(f"Successfully processed {os.path.basename(path)}: {result}")
        except Exception as e:
            logging.error(f"Failed to process {path}: {e}")

if __name__ == "__main__":
    run_batch_processing("metadata.csv")