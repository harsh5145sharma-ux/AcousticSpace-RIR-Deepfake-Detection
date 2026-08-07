import os
import joblib
import numpy as np
import librosa

LABEL_MAPPING = {0: 'bonafide', 1: 'spoof'}

class DeepfakeInferenceEngine:
    def __init__(self, model_path='models/checkpoint.pkl'):
        self.model_path = model_path
        self.model = self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f'Model checkpoint not found at {self.model_path}.')
        return joblib.load(self.model_path)

    def predict(self, features):
        features_array = np.array(features)
        if features_array.ndim == 1:
            features_array = features_array.reshape(1, -1)
        prediction_class = int(self.model.predict(features_array)[0])
        if hasattr(self.model, 'predict_proba'):
            probabilities = self.model.predict_proba(features_array)[0]
            confidence = float(np.max(probabilities))
        else:
            confidence = 0.95
        is_fake = bool(prediction_class == 1)
        return {'is_fake': is_fake, 'confidence': confidence, 'label': LABEL_MAPPING.get(prediction_class, 'unknown')}

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = DeepfakeInferenceEngine()
    return _engine

def predict_audio(audio_path: str):
    engine = get_engine()
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f'Audio file not found at: {audio_path}')
    y, sr = librosa.load(audio_path, sr=16000)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    features = np.mean(mfccs.T, axis=0)
    return engine.predict(features)

def predict(audio_path: str):
    return predict_audio(audio_path)