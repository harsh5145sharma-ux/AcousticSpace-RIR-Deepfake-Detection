import pandas as pd
import os

def get_audio_paths(csv_path):
    df = pd.read_csv(csv_path)
    return df['filename'].tolist()

def get_full_path(filename, base_dir="data"):
     return os.path.join(base_dir, filename)