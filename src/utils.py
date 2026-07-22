import librosa  # type: ignore[import]
import numpy as np

def audio_to_spectrogram(file_path):
    y, sr = librosa.load(file_path, sr=22050)
    spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    spec = librosa.power_to_db(spec, ref=np.max)
    
    # Ensure exact 128x128 shape
    target_width = 128
    current_width = spec.shape[1]
    
    if current_width < target_width:
        # Pad with zeros if too short
        padding = target_width - current_width
        spec = np.pad(spec, ((0, 0), (0, padding)), mode='constant')
    else:
        # Crop to 128 if too long
        spec = spec[:, :target_width]
        
    return spec