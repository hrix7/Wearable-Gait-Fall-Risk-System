# Synthetic gait benchmark provenance

No participant, IMU recording or clinical dataset is used. `pipeline.py` constructs a 20-second acceleration-magnitude surrogate at 50 Hz: a 1 g baseline plus Gaussian pulses of amplitude 0.25 g and width parameter 0.04 seconds. Analytic pulse centers start at 0.75 seconds and recur at 90, 120 or 150 steps/minute, stopping 0.5 seconds before the record ends. These centers are the reference events, independent of detector output. Gaussian noise SD is 0.01, 0.06 or 0.12 g. The fixed random seed is 1729; the same standardized noise realization is reused across conditions, making comparisons paired, not independent replicates.

The existing SciPy prominence detector uses 0.15 g prominence and at least 0.3 seconds between detections. Event matching uses a fixed ±0.15 second tolerance, one-to-one and ordered, maximizing matches before minimizing absolute timing error. Precision/recall/F1, timing MAE, cadence and absolute cadence error are calculated, not hand-entered. Undefined values are JSON null. No parameter was tuned against the exported test conditions.

This is a deterministic software regression benchmark. It omits human gait morphology, sensor placement, motion artifacts, missing packets, posture and inter-person variation. The nine conditions are a scenario grid, not a population sample; no confidence interval or clinical fall-risk prediction is implied. The historical academic IMU/FSR/PPG concept is distinct from the new acceleration-only synthetic benchmark.

Dependencies are pinned in requirements.txt. Retain the source commit, config.json, source/data/config SHA-256 values in results/results.json and results/manifest.json. The verifier recomputes all artifacts in the same environment. Last floating-point bits can vary across environments. Original project ownership and rights remain governed by LICENSE; no third-party datasets are redistributed.


November 28 diagnostic extension: Prominence-minus-fixed-height F1 on identical flattened-gap noise realizations, separately against nominal/present reference events; signed descriptive ranges, direction counts and defined-pair counts. Noise seeds are not human participants; no population interval or detector selection. Existing primary generator, seeds and detector/model settings are unchanged.
