from src.utils import audio_to_spectrogram
import numpy as np

def test_padding():
    # This acts as a dummy path; in reality, point this to a test .wav file
    spec = audio_to_spectrogram("tests/test_audio.wav")
    assert spec.shape == (128, 128)
    print("Test passed: Shape is 128x128")

if __name__ == "__main__":
    test_padding()