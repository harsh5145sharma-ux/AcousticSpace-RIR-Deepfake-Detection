# Dataset Analysis Report — ASVspoof (RIR Pipeline)

**Prepared by:** Member 1 — ML / Audio Pipeline Lead
**Project:** AcousticSpace — Deepfake Detection via Room Impulse Response
**Status:** Living document — update after each dataset pull / cleaning pass

---

## 1. Dataset Overview

| Item | Detail |
|---|---|
| Source | ASVspoof (fill in exact edition, e.g. ASVspoof 2019 LA / 2021 DF) |
| Access | Fill in: download link, license terms, request-access status |
| Format | FLAC, 16kHz, mono |
| Splits used | train / dev / eval (confirm which splits this project uses) |
| Protocol file(s) | `protocol.txt` — speaker_id, file_id, system_id, label |
| Classes | `bonafide` (genuine) vs `spoof` (synthetic/converted/replayed) |

> Fill in the actual class counts and split sizes once the dataset is downloaded.
> Template table below — replace with real numbers.

| Split | Bonafide | Spoof | Total |
|---|---|---|---|
| Train | — | — | — |
| Dev | — | — | — |
| Eval | — | — | — |

---

## 2. Data Quality Checks

The pipeline (`preprocessing.py`) performs the following automatic checks on ingest:

- **Corrupt/unreadable files** — caught via `soundfile` read errors, logged and skipped.
- **Too-short clips** — anything under `MIN_DURATION_SEC` (default 0.3s) after silence
  trimming is dropped, since these don't carry a usable reverberant tail for RIR features.
- **Silence trimming** — `librosa.effects.trim` (30dB threshold) removes leading/trailing
  silence so RT60/EDT estimates aren't skewed by dead air.
- **Sample rate mismatch** — anything not already at 16kHz is resampled.
- **Clipping/peak normalization** — all clips peak-normalized to avoid amplitude bias in
  spectral features.

Run the pipeline with `--protocol` pointed at each split and check the logged
"Processed N files, skipped M" line — M should be near zero on a clean download.
If M is high, re-download or check the protocol file matches the audio directory.

---

## 3. Feature Set

| Feature | What it captures | Why it matters for spoof detection |
|---|---|---|
| RT60 | Reverberation time (T20-extrapolated) | Genuine recordings carry room reverb; many TTS/VC systems don't reproduce a physically consistent decay |
| EDT | Early Decay Time | Sensitive to the very early reflections, often distorted in synthetic audio |
| C50 | Clarity index (early/late energy ratio) | Synthetic audio tends toward anomalously high clarity (little/no natural reverb tail) |
| Spectral centroid / bandwidth / rolloff | Timbral shape | Vocoder artifacts shift spectral energy distribution vs. natural speech |
| Zero-crossing rate | Noisiness / high-frequency content | Flags unnatural high-frequency artifacts from some synthesis methods |
| MFCC (13 coeffs) | Standard speech representation | Baseline features for the classifier; also fed to Member 2's AST model as needed |
| RMS energy | Loudness envelope | Sanity/normalization check, secondary signal |

Full extraction logic lives in `preprocessing.py`; see `notebooks/feature_extraction.ipynb`
for a worked example with plots.

---

## 4. Known Risks / Open Questions

- [ ] Confirm which ASVspoof edition/track the team is standardizing on (LA vs PA vs DF) —
      this changes what "spoof" means (synthesis vs. replay attack) and may need different
      RIR feature emphasis.
- [ ] Class imbalance: ASVspoof splits are typically spoof-heavy in eval; check if
      re-weighting or stratified sampling is needed before handing off to Member 2.
- [ ] Decide the canonical `--ext` (flac vs wav) once real data is downloaded, and update
      the pipeline default accordingly.
- [ ] Cross-check RT60/EDT estimates against a small hand-labeled subset to validate they
      behave as expected before trusting them as model features at scale.

---

## 5. Next Steps (Week 1 → Week 2 handoff to Member 2)

1. Run `preprocessing.py` over full train/dev splits → produce `features.csv` per split.
2. Sanity-check class-wise feature distributions (see notebook Section 6) for separability.
3. Freeze the feature schema (documented in `preprocessing.py` docstring) so Member 2 can
   build the AST training loader against a stable column set.
4. Log dataset stats (Section 1 table) and quality-check results (Section 2) here after
   the real download — this file should reflect actual figures before Week 1 ends.
