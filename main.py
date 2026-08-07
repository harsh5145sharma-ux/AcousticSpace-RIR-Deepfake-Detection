import os
import logging
import numpy as np
import pandas as pd
from src.data_loader import get_audio_paths
from src.utils import audio_to_spectrogram
from models.inference import get_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_batch_processing(csv_file):
    paths = get_audio_paths(csv_file)
    logging.info(f"Starting batch for {len(paths)} files.")
    
    if not os.path.exists("processed"):
        os.makedirs("processed")
    
    engine = get_engine()
    for path in paths:
        try:
            y, sr = librosa.load(path, sr=16000)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
            features = np.mean(mfccs.T, axis=0)
            
            file_name = os.path.basename(path).replace(".wav", ".npy")
            save_path = os.path.join("processed", file_name)
            np.save(save_path, features)
        
            result = engine.predict(features)
            logging.info(f"Saved {file_name}. Processed: {result}")

        except Exception as e:
            logging.error(f"Failed to process {path}: {e}")

if __name__ == "__main__":
    import librosa
    run_batch_processing("metadata.csv")