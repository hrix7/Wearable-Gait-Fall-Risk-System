# Wearable Gait and Fall-Risk Sensor System

I designed this multimodal wearable-system concept at Arizona State University under Aurel Coza. I combined IMU, force-sensitive resistor (FSR), and photoplethysmography (PPG) measurements to describe gait, balance, cardiovascular response, and potential fall-risk indicators.

## Work I completed

- Defined the sensing architecture and the role of each sensor.
- Developed step, stride, sway, and left-right symmetry measures.
- Used acceleration magnitude for candidate step detection.
- Incorporated PPG-derived heart-rate information into the monitoring concept.
- Planned FSR-based stance and loading measurements.
- Designed a clinician-facing dashboard mock-up for reviewing trends and flagged metrics.
- Documented a validation approach for comparing sensor-derived measures with reference observations.

## System features

- IMU-based step and sway analysis.
- FSR-based stance and load distribution.
- PPG-based heart-rate monitoring.
- Gait symmetry and cadence summaries.
- Modular outputs that can feed a clinician-facing dashboard.

## Repository code

- `src/step_detection.py` detects candidate steps from acceleration magnitude.
- `src/gait_summary.py` converts detected step times into cadence and interval-variability measures.
- `examples/acceleration.csv` provides a small demonstration input.
- `docs/VALIDATION.md` describes the validation strategy and limits.

## Run the example

```bash
python -m pip install -r requirements.txt
python src/step_detection.py examples/acceleration.csv --sample-rate 50
python src/gait_summary.py examples/acceleration.csv --sample-rate 50
```

## Tools

Python, MATLAB, NumPy, pandas, SciPy, signal processing, IMU, FSR, PPG, wearable-system design.

## Scope

This is an academic prototype and analysis portfolio, not a diagnostic or clinically validated fall-prediction device.

## Author and Project Setting

**Author:** Hritika Adhikary  
**Project:** Graduate Wearable Technologies Project  
**Institution:** Arizona State University  
**Faculty Advisor:** Aurel Coza  
**Period:** Fall 2025

## Rights

Copyright (c) 2026 Hritika Adhikary. All rights reserved. See [LICENSE](LICENSE).

## Reproducible synthetic benchmark

The academic multimodal concept now has an acceleration-only software benchmark: three cadences × three noise levels, known synthetic step times, and measured detection/timing/cadence errors. This is not participant data or validated fall-risk prediction. See [provenance](DATA_PROVENANCE.md), [computed report](results/report.md) and [development backlog](DEVELOPMENT_BACKLOG.md).

```sh
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 pipeline.py
python3 pipeline.py --verify
```

The verifier recomputes data, metrics, reports and checksums and refuses mismatches. `--output DIR` supports isolated results. Dependencies are pinned. Candidate events must be strictly increasing nonnegative sample indices; missing/insufficient cadence estimates remain undefined rather than zero.

GitHub Actions validates pushes, pull requests, manual requests and daily runs at 10:07 UTC. It has read-only repository access and uploads verified report artifacts; it does not modify source or require secrets. Source development is handled by the separate daily development schedule, with tests before pushes. All actions are pinned to commit SHAs.

## 2026-11-13 benchmark extension

Adds a predeclared 0.125 g threshold above record median, local maxima and chronological refractory selection. It does not call the main SciPy prominence detector, and its thresholds are not selected on this evaluation grid. Both detectors use the same minimum interval and analytic references; results include baseline event FP/FN/F1 for every existing condition. A baseline is not clinical validation.

## 2026-11-14 extension

Adds nine stress cases with independently seeded uniform timing offsets, half-width min(0.06 s, 0.2 periods), plus full jitter_data.csv and fingerprints. Actual perturbed centers define event truth; nominal cadence remains a generator setting. Both detectors are evaluated without tuning; the original nine regular-timing cases are retained.

## 2026-11-15 correctness extension

Adds interval_count and sample_interval_cv_percent (sample SD, ddof=1), undefined with fewer than two intervals. Existing interval_cv_percent retains population SD, ddof=0, so historical semantics are preserved. The sample-CV ratio is not claimed to be an unbiased estimator or a clinical fall-risk score.

## Flattened-signal gap scenarios

Added nine deterministic finite flattening scenarios: replace [0.4T,0.5T) by 1 g while retaining timestamps. Evaluate separately against nominal events and reference centers outside the gap. This is not support for real NaN/missing samples, participant gait, or clinical fall-risk prediction. Full-precision masked signal hashes reproduce from the generator/config, not the rounded base CSV. Tests cover mask boundaries, invalid intervals, reference accounting and exact regeneration.

## Paired additive motion-burst scenarios

Nine motion conditions add a fixed 0.4 g, 2.7 Hz sinusoid under a sin-squared envelope on [0.3T,0.6T). Original pulse centers and paired noise are unchanged. Both predeclared detectors are scored against independent event truth. Tests check analytic envelope samples, exact untouched boundaries, invalid inputs, full-precision signal hashes and independently recomputed metrics. This is a teaching acceleration surrogate, not measured participant motion or clinical fall-risk validation.

## Independent noise-realization sensitivity

Added ten predeclared noise seeds per cadence/noise cell with fixed regular event times and detector. Reports each replicate hash/metrics plus descriptive F1 min/mean/max and defined-value count. This measures within-cell noise-only sensitivity, not population uncertainty, confidence intervals or clinical fall risk. Realizations are paired across cells and must not be pooled as independent samples. Original benchmark seeds/results remain separate. Tests independently reconstruct each signal/metric, verify seed-invariant zero-noise output and validate seed specifications.

## Paired motion effects over noise realizations

Each predeclared noise realization now applies the same fixed motion burst to its own base signal, preserving independent event truth. Reports motion signal hashes/F1 and original-minus-motion paired F1 min/mean/max, including negative differences when motion happens to improve scores. These are descriptive noise-only pairs, not confidence intervals or subject-population claims. Tests reconstruct hashes/scores and use identity perturbations to prove exactly zero paired effect.

### November 21 development

Each existing noise replicate now exports independently reproducible gap-signal hash and both nominal-reference and present-reference metrics/counts. Original and motion conditions retained. Reconstruct gaps via independent sample assignment and recompute both event populations. Descriptive synthetic scenario results, not missing-value handling or population uncertainty.
