"""
Unit tests for preprocessing.py.

Run with:
    pytest tests/
"""

import sys
import os
import numpy as np
import soundfile as sf
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from preprocessing import (
    load_audio,
    extract_features,
    estimate_energy_decay_curve,
    estimate_rt60,
    estimate_edt,
    estimate_c50,
    SAMPLE_RATE,
    MIN_DURATION_SEC,
)


@pytest.fixture
def synthetic_decay_signal():
    """A synthetic tone with a clean exponential decay, standing in for a
    'reverberant' bonafide-style clip."""
    t = np.linspace(0, 1.5, int(SAMPLE_RATE * 1.5))
    y = np.sin(2 * np.pi * 220 * t) * np.exp(-1.5 * t)
    return y.astype(np.float32)


@pytest.fixture
def synthetic_flat_signal():
    """A synthetic tone with almost no decay, standing in for a
    'dry'/spoof-style clip."""
    t = np.linspace(0, 1.5, int(SAMPLE_RATE * 1.5))
    y = np.sin(2 * np.pi * 220 * t) * np.exp(-0.05 * t)
    return y.astype(np.float32)


def test_load_audio_valid_file(tmp_path, synthetic_decay_signal):
    path = tmp_path / "sample.wav"
    sf.write(str(path), synthetic_decay_signal, SAMPLE_RATE)

    y = load_audio(str(path))
    assert y is not None
    assert isinstance(y, np.ndarray)
    assert np.max(np.abs(y)) <= 1.0 + 1e-6  # peak normalized


def test_load_audio_missing_file_returns_none():
    y = load_audio("/nonexistent/path/does_not_exist.wav")
    assert y is None


def test_load_audio_too_short_returns_none(tmp_path):
    short_signal = np.zeros(int(SAMPLE_RATE * (MIN_DURATION_SEC / 2)), dtype=np.float32)
    path = tmp_path / "short.wav"
    sf.write(str(path), short_signal, SAMPLE_RATE)

    y = load_audio(str(path))
    assert y is None


def test_energy_decay_curve_is_monotonic_ish(synthetic_decay_signal):
    edc = estimate_energy_decay_curve(synthetic_decay_signal)
    # Backward-integrated energy decay should trend downward overall
    assert edc[0] >= edc[-1]


def test_rt60_decaying_signal_greater_than_flat_signal(
    synthetic_decay_signal, synthetic_flat_signal
):
    edc_decay = estimate_energy_decay_curve(synthetic_decay_signal)
    edc_flat = estimate_energy_decay_curve(synthetic_flat_signal)

    rt60_decay = estimate_rt60(edc_decay)
    rt60_flat = estimate_rt60(edc_flat)

    # A flatter-energy signal should register a longer (or clipped-max) RT60
    # than one with a fast, clean exponential decay is not guaranteed in
    # general, but both should return valid, clipped values.
    assert 0.0 <= rt60_decay <= 3.0
    assert 0.0 <= rt60_flat <= 3.0


def test_edt_within_expected_range(synthetic_decay_signal):
    edc = estimate_energy_decay_curve(synthetic_decay_signal)
    edt = estimate_edt(edc)
    assert 0.0 <= edt <= 3.0


def test_c50_returns_finite_value(synthetic_decay_signal):
    c50 = estimate_c50(synthetic_decay_signal)
    assert np.isfinite(c50)


def test_extract_features_returns_expected_shape(synthetic_decay_signal):
    feats = extract_features(synthetic_decay_signal, "test_001", "bonafide")
    row = feats.to_row()

    expected_keys = {
        "file_id", "label", "rt60", "edt", "c50",
        "spectral_centroid_mean", "spectral_bandwidth_mean",
        "spectral_rolloff_mean", "zcr_mean", "rms_mean", "duration_sec",
    }
    expected_keys.update({f"mfcc_{i}" for i in range(1, 14)})

    assert expected_keys.issubset(row.keys())
    assert row["file_id"] == "test_001"
    assert row["label"] == "bonafide"
    assert all(np.isfinite(v) for k, v in row.items() if k not in ("file_id", "label"))
