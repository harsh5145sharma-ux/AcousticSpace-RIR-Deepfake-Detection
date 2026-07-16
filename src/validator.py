import numpy as np

def validate_input(file_path):
    """Validates that the input .npy file matches the expected (128, 128) shape."""
    try:
        data = np.load(file_path)
        if data.shape != (128, 128):
            raise ValueError(f"CONTRACT ERROR: Expected shape (128, 128), got {data.shape}")
        print("Validation successful: Data shape is (128, 128).")
        return True
    except Exception as e:
        print(f"Validation failed: {e}")
        return False