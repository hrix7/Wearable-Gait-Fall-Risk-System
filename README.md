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

**Hritika Adhikary**  
Graduate Wearable Technologies Project, Arizona State University  
Faculty Advisor: Aurel Coza  
Fall 2025

## Rights

Copyright (c) 2026 Hritika Adhikary. All rights reserved. See [LICENSE](LICENSE).
