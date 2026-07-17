import librosa
import numpy as np
import pandas as pd
import os
import json

def extract_rir_features(audio_path):
    """
    Dummy RIR feature extraction.
    Placeholder for actual RIR logic.
    """
    y, sr = librosa.load(audio_path, sr=None)
    # Placeholder: MFCCs as a proxy for RIR features for pipeline testing
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs, axis=1)

def process_dataset(metadata_path, output_dir):
    df = pd.read_csv(metadata_path)
    features = []
    
    for _, row in df.iterrows():
        # Using row['before_path'] as the audio file source
        # Mapping to local path for pipeline processing
        audio_path = os.path.join("/workspace/inputs", os.path.basename(row['before_path']))
        
        # NOTE: This assumes files are available. 
        # In actual execution, verify existence of files.
        try:
            feats = extract_rir_features(audio_path)
            features.append({
                "filename": row['filename'],
                "label": row['label'],
                "features": feats.tolist()
            })
        except Exception as e:
            print(f"Error processing {audio_path}: {e}")
            
    with open(os.path.join(output_dir, 'dataset_features.json'), 'w') as f:
        json.dump(features, f)

if __name__ == "__main__":
    output_dir = "/workspace/member1_work"
    metadata_path = "/workspace/inputs/metadata-4543.csv"
    process_dataset(metadata_path, output_dir)
