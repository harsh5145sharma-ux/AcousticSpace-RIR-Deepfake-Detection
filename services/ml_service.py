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


def get_predictor():

    candidates = [
        ("models.inference", "predict"),
        ("models.inference", "predict_audio"),
        ("inference", "predict"),
        ("inference", "predict_audio"),
        ("src.inference", "predict"),
    ]

    function = _find_callable(candidates)

    if function is None:
        raise MLIntegrationError(
            "Member 2 model inference is not integrated yet."
        )

    return function


def normalize_result(raw_result):

    if not isinstance(raw_result, dict):
        raise MLIntegrationError(
            "Model must return a dictionary."
        )

    # -----------------------------
    # prediction
    # -----------------------------

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
        "1",
    }

    real_labels = {
        "real",
        "human",
        "genuine",
        "authentic",
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

    # -----------------------------
    # confidence
    # -----------------------------

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


def predict_audio_file(file_path):

    preprocessing = get_preprocessor()

    predictor = get_predictor()

    try:

        features = preprocessing(
            file_path
        )

    except Exception as exc:

        raise MLIntegrationError(
            f"Preprocessing failed: {exc}"
        ) from exc

    if features is None:

        raise MLIntegrationError(
            "Preprocessing returned no features."
        )

    try:

        raw_result = predictor(
            features
        )

    except Exception as exc:

        raise MLIntegrationError(
            f"Model inference failed: {exc}"
        ) from exc

    return normalize_result(
        raw_result
    )


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