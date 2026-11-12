# Synthetic gait event benchmark

Known pulse centers are reference events. All values below are measured by the detector; no clinical validity is claimed.

| Cadence (steps/min) | Noise SD (g) | TP | FP | FN | F1 | Timing MAE (s) | Cadence error (steps/min) |
|---|---|---|---|---|---|---|---|
| 90 | 0.01 | 29 | 0 | 0 | 1 | 0.006092 | 0.06424 |
| 90 | 0.06 | 29 | 9 | 0 | 0.8657 | 0.01598 | 26.84 |
| 90 | 0.12 | 26 | 24 | 3 | 0.6582 | 0.03077 | 59.69 |
| 120 | 0.01 | 38 | 0 | 0 | 1 | 0.01 | 0.1296 |
| 120 | 0.06 | 38 | 1 | 0 | 0.987 | 0.01579 | 0 |
| 120 | 0.12 | 34 | 6 | 4 | 0.8718 | 0.02412 | 0.8554 |
| 150 | 0.01 | 47 | 0 | 0 | 1 | 0.01 | 0.1629 |
| 150 | 0.06 | 47 | 1 | 0 | 0.9895 | 0.01426 | 1.579 |
| 150 | 0.12 | 45 | 4 | 2 | 0.9375 | 0.02644 | 3.36 |

One-to-one matching maximizes event matches within the fixed tolerance, then minimizes total absolute timing error. Cadence uses the interval between detected steps, not total record duration. See DATA_PROVENANCE.md for assumptions, source versions and limitations.

Result SHA-256: `b29e513cf0facd3253cbc5665365b4166c35bb1205ab271a76f4f46aeb916842`
