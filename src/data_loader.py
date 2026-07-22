import pandas as pd
import os

def get_audio_paths(csv_path, data_dir="data"):
    df = pd.read_csv(csv_path)
    valid_paths = []
    for f in df['filename']:
        full_path = os.path.join(data_dir, f)
        if os.path.exists(full_path):
            valid_paths.append(full_path)
        else:
            print(f"Skipping missing file: {f}")
    return valid_paths