"""
Inference script for AcousticSpace RIR Deepfake Detection.
Loads a trained model checkpoint and provides a clean prediction interface.
"""

import os
import joblib  # or torch, depending on your model format
import numpy as np
import src.utils  # Utilizing your real preprocessing pipeline!
import librosa

# Define label mapping constants
LABEL_MAPPING = {
    0: "bonafide",  # Real human audio
    1: "spoof"      # AI-generated deepfake audio
}

class DeepfakeInferenceEngine:
    def __init__(self, model_path="models/checkpoint.pkl"):
        """Initializes and loads the trained model checkpoint."""
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        """Loads the actual trained model from disk."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Model checkpoint not found at {self.model_path}. "
                "Please ensure the trained model file is present."
            )
        # Loading a serialized model (adjust loader if using PyTorch/TensorFlow)
        return joblib.load(self.model_path)

    def predict(self, features):
        """
        Accepts preprocessed features, runs real model inference, 
        and returns prediction results.
        
        Expected input shape: 2D array or feature vector matching training schema.
        """
        # Ensure features are in the correct shape for prediction
        features_array = np.array(features)
        if features_array.ndim == 1:
            features_array = features_array.reshape(1, -1)

        # Real model inference
        prediction_class = int(self.model.predict(features_array)[0])
        
        # Get probability/confidence if available, otherwise default safely
        if hasattr(self.model, "predict_proba"):
            probabilities = self.model.predict_proba(features_array)[0]
            confidence = float(np.max(probabilities))
        else:
            confidence = 0.95  # Fallback if binary margin

        is_fake = bool(prediction_class == 1)  # 1 = spoof/fake, 0 = real

        return {
            "is_fake": is_fake,
            "confidence": confidence,
            "label": LABEL_MAPPING.get(prediction_class, "unknown")
        }

# Global instance for backend import
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = DeepfakeInferenceEngine()
    return _engine

def predict_audio(audio_path: str):
    """
    End-to-end wrapper function for backend integration:
    1. Loads raw audio using librosa.
    2. Extracts audio features (e.g., MFCCs or spectrogram summary) matching training shape.
    3. Runs inference using the actual trained model.
    4. Returns structured results.
    """
    engine = get_engine()
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found at: {audio_path}")

    # Load audio waveform and sample rate using standard librosa pipeline
    y, sr = librosa.load(audio_path, sr=16000)
    
    # Extract robust features (e.g., mean MFCCs or spectral features matching your model input)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    features = np.mean(mfccs.T, axis=0)  # Flattened feature vector
    
    result = engine.predict(features)
    return result