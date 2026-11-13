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

## Independent fixed-height baseline

Predeclared threshold: 0.125 g above record median, local maxima, chronological refractory spacing identical to the main detector. No evaluation-grid tuning. Not a clinical comparator.

| Cadence | Noise SD | Baseline FP | Baseline FN | Baseline F1 |
|---|---|---|---|---|
| 90 | 0.01 | 0 | 0 | 1 |
| 90 | 0.06 | 4 | 3 | 0.8814 |
| 90 | 0.12 | 23 | 5 | 0.6316 |
| 120 | 0.01 | 0 | 0 | 1 |
| 120 | 0.06 | 2 | 1 | 0.961 |
| 120 | 0.12 | 20 | 10 | 0.6512 |
| 150 | 0.01 | 0 | 0 | 1 |
| 150 | 0.06 | 1 | 0 | 0.9895 |
| 150 | 0.12 | 6 | 4 | 0.8958 |

Result SHA-256: `1ee79483dc1f90b14e39971362d9b11cf7c6ac38cdd576390fbf8ef9d0ff81ae`
