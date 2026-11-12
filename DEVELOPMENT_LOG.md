# Development log

## 2026-11-12 — reproducible gait event benchmark

Added nine fixed synthetic cadence/noise conditions with known event centers, independent of detector output. Ordered one-to-one matching maximizes true positives before minimizing timing error; no detection can count twice. Reports include false positives, false negatives, F1, timing MAE and cadence error. Detector inputs and summary indices now reject invalid/nonfinite values. Minimum detection spacing uses the ceiling in samples so it cannot round below the requested physical interval.

Local validation: Python 3.11.0; 17 tests, deterministic export, independent recomputation, artifact tamper rejection, diff whitespace check and actionlint 1.7.12. Pinned numpy 2.2.6, pandas 2.3.2 and scipy 1.16.2 match the installed runtime. Shellcheck is not available locally. Hosted validation is linked from the repository Actions page and is checked after publication.

No participant data, clinical fall-risk model or completed multimodal device validation is implied. The existing academic IMU/FSR/PPG concept remains distinct from this new synthetic acceleration-only benchmark.
