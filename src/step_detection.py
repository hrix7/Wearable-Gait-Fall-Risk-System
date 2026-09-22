"""Detect candidate steps from acceleration magnitude."""
from __future__ import annotations
import argparse
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def detect_steps(acceleration, sample_rate_hz: float, min_interval_s: float = 0.3,
                 prominence: float = 0.15) -> np.ndarray:
    signal = np.asarray(acceleration, dtype=float)
    if signal.ndim != 1 or signal.size < 3:
        raise ValueError("acceleration must be a one-dimensional signal")
    centered = signal - np.median(signal)
    distance = max(1, round(sample_rate_hz * min_interval_s))
    peaks, _ = find_peaks(centered, distance=distance, prominence=prominence)
    return peaks

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--sample-rate", type=float, required=True)
    args = parser.parse_args()
    frame = pd.read_csv(args.csv)
    peaks = detect_steps(frame["acceleration_g"], args.sample_rate)
    print(f"Detected {len(peaks)} candidate steps")
    print("Peak indices:", peaks.tolist())
