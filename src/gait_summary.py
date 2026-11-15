"""Summarize cadence and step-interval variability from my wearable signals."""
from __future__ import annotations
import argparse
import json
import math
import numpy as np
import pandas as pd
from step_detection import detect_steps

def summarize_steps(indices, sample_rate_hz: float) -> dict[str, float | int | None]:
    raw = np.asarray(indices, dtype=float)
    if raw.ndim != 1 or not np.isfinite(raw).all() or np.any(raw < 0) or np.any(raw != np.floor(raw)):
        raise ValueError("step indices must be a one-dimensional array of finite nonnegative integers")
    if raw.size > 1 and np.any(np.diff(raw) <= 0):
        raise ValueError("step indices must be strictly increasing")
    peaks = raw
    if not math.isfinite(sample_rate_hz) or sample_rate_hz <= 0:
        raise ValueError("sample_rate_hz must be finite and positive")
    if peaks.size < 2:
        return {"steps": int(peaks.size), "cadence_spm": None,
                "mean_interval_s": None, "interval_cv_percent": None,
                "interval_count": 0,"sample_interval_cv_percent": None}
    intervals = np.diff(peaks) / sample_rate_hz
    mean_interval = float(intervals.mean())
    return {
        "steps": int(peaks.size),
        "interval_count": int(intervals.size),
        "sample_interval_cv_percent": float(100.0 * intervals.std(ddof=1) / mean_interval) if intervals.size>=2 else None,
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
