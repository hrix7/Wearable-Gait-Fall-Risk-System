# Wearable Gait and Fall-Risk System

A modular research prototype for working with IMU, FSR, and PPG signals used in gait and fall-risk studies.

## Capabilities represented

- Accelerometer-based step detection
- PPG heart-rate estimation
- Gait symmetry and sway feature planning
- Sensor-fusion architecture
- Clinician-facing dashboard concepts

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/step_detection.py examples/acceleration.csv --sample-rate 50
```

The included CSV is synthetic and exists only to exercise the code.

## Structure

- `src/`: signal-processing utilities
- `examples/`: synthetic sensor data
- `docs/`: measurement and validation notes

## Validation status

This is educational/research software. It does not estimate clinical fall risk and must not be used for medical decision-making without appropriate validation.

## License

MIT.
