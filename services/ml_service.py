"""
ML integration layer.

Member 1:
preprocessing

Member 2:
model inference

Member 3:
backend integration
"""

from importlib import import_module


class MLIntegrationError(Exception):
    """Raised when ML pipeline integration fails."""
    pass


def _find_callable(candidates):
    for module_name, function_name in candidates:
        try:
            module = import_module(module_name)

            function = getattr(
                module,
                function_name,
                None,
            )

            if callable(function):
                return function

        except (ImportError, ModuleNotFoundError):
            continue

    return None


# ============================================================
# MEMBER 1 - PREPROCESSING
# ============================================================

def get_preprocessor():
    candidates = [
        ("preprocessing", "preprocess_audio"),
        ("preprocessing", "process_audio"),
        ("preprocessing", "extract_features"),
        ("src.preprocessing", "preprocess_audio"),
        ("src.preprocessing", "extract_features"),
    ]

    function = _find_callable(candidates)

    if function is None:
        raise MLIntegrationError(
            "Member 1 preprocessing is not integrated yet."
        )

    return function


# ============================================================
# MEMBER 2 - MODEL INFERENCE
# ============================================================

def get_predictor():
    candidates = [
        ("ml_models.inference", "predict_audio"),
        ("ml_models.inference", "predict"),
        ("models.inference", "predict_audio"),
        ("models.inference", "predict"),
        ("inference", "predict_audio"),
        ("inference", "predict"),
        ("src.inference", "predict"),
    ]

    function = _find_callable(candidates)

    if function is None:
        raise MLIntegrationError(
            "Member 2 model inference is not integrated yet."
        )

    return function


# ============================================================
# NORMALIZE MEMBER 2 RESULT
# ============================================================

def normalize_result(raw_result):
    if not isinstance(raw_result, dict):
        raise MLIntegrationError(
            "Model must return a dictionary."
        )

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    if "is_fake" in raw_result:
        prediction = (
            "fake"
            if bool(raw_result["is_fake"])
            else "real"
        )

    elif "prediction" in raw_result:
        prediction = str(
            raw_result["prediction"]
        ).lower().strip()

    elif "label" in raw_result:
        prediction = str(
            raw_result["label"]
        ).lower().strip()

    else:
        raise MLIntegrationError(
            "Model result missing prediction."
        )

    fake_labels = {
        "fake",
        "ai",
        "deepfake",
        "synthetic",
        "generated",
        "spoof",
        "1",
    }

    real_labels = {
        "real",
        "human",
        "genuine",
        "authentic",
        "bonafide",
        "bona_fide",
        "0",
    }

    if prediction in fake_labels:
        prediction = "fake"

    elif prediction in real_labels:
        prediction = "real"

    else:
        raise MLIntegrationError(
            f"Unknown prediction label: {prediction}"
        )

    # --------------------------------------------------------
    # Confidence
    # --------------------------------------------------------

    confidence = raw_result.get(
        "confidence",
        raw_result.get(
            "probability",
            raw_result.get(
                "score",
                0.0,
            ),
        ),
    )

    try:
        confidence = float(confidence)

    except (TypeError, ValueError):
        raise MLIntegrationError(
            "Invalid model confidence."
        )

    if confidence > 1:
        confidence = confidence / 100

    confidence = max(
        0.0,
        min(confidence, 1.0),
    )

    return {
        "prediction": prediction,
        "confidence": confidence,
        "flagged_segments": raw_result.get(
            "flagged_segments",
            [],
        ),
    }


# ============================================================
# COMPLETE AUDIO PREDICTION PIPELINE
# ============================================================

def predict_audio_file(file_path):
    """
    Run complete prediction pipeline.

    Member 1 preprocessing is checked to ensure that the
    preprocessing component is integrated.

    Member 2 predict_audio() receives the original audio path
    because Member 2's trained model uses its own 40-MFCC
    inference preprocessing.
    """

    # --------------------------------------------------------
    # Verify Member 1 integration
    # --------------------------------------------------------

    preprocessor = get_preprocessor()

    try:
        member1_features = preprocessor(file_path)

    except Exception as exc:
        raise MLIntegrationError(
            f"Member 1 preprocessing failed: {exc}"
        ) from exc

    if member1_features is None:
        raise MLIntegrationError(
            "Member 1 preprocessing returned no features."
        )

    # --------------------------------------------------------
    # Member 2 actual model inference
    # --------------------------------------------------------

    predictor = get_predictor()

    try:
        # IMPORTANT:
        # Member 2 predict_audio() expects AUDIO FILE PATH,
        # not Member 1's 22-feature array.
        raw_result = predictor(file_path)

    except Exception as exc:
        raise MLIntegrationError(
            f"Member 2 model inference failed: {exc}"
        ) from exc

    return normalize_result(raw_result)


# ============================================================
# INTEGRATION STATUS
# ============================================================

def integration_status():
    member1 = False
    member2 = False

    try:
        get_preprocessor()
        member1 = True

    except MLIntegrationError:
        pass

    try:
        get_predictor()
        member2 = True

    except MLIntegrationError:
        pass

    return {
        "backend": True,
        "member1_preprocessing": member1,
        "member2_inference": member2,
        "pipeline_ready": member1 and member2,
    }