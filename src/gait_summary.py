"""Summarize cadence and step-interval variability from my wearable signals."""
from __future__ import annotations
import argparse
import json
import numpy as np
import pandas as pd
from step_detection import detect_steps

def summarize_steps(indices, sample_rate_hz: float) -> dict[str, float | int | None]:
    peaks = np.asarray(indices, dtype=int)
    if sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be positive")
    if peaks.size < 2:
        return {"steps": int(peaks.size), "cadence_spm": None,
                "mean_interval_s": None, "interval_cv_percent": None}
    intervals = np.diff(peaks) / sample_rate_hz
    mean_interval = float(intervals.mean())
    return {
        "steps": int(peaks.size),
        "cadence_spm": float(60.0 / mean_interval),
        "mean_interval_s": mean_interval,
        "interval_cv_percent": float(100.0 * intervals.std(ddof=0) / mean_interval),
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--sample-rate", type=float, required=True)
    args = parser.parse_args()
    frame = pd.read_csv(args.csv)
    peaks = detect_steps(frame["acceleration_g"], args.sample_rate)
    print(json.dumps(summarize_steps(peaks, args.sample_rate), indent=2))
