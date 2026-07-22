def predict(spectrogram):
    """
    Mock inference function. 
    In the future, this will be replaced with a real call to the AST model.
    """
    # Returning a dummy prediction: is_fake=True, confidence=0.87
    return {
        "is_fake": True,
        "confidence": 0.87,
        "flagged_segments": [[2.1, 3.4]]
    }