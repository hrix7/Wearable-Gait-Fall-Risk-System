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

## Bounded timing jitter

Reference centers have independent-seed uniform offsets (half-width min(0.06 s, 0.2 periods)); observation noise stream is unchanged. Actual perturbed centers define truth, not a regular schedule. Full samples are in jitter_data.csv.

| Nominal cadence | Noise SD | Half-width (s) | FP | FN | F1 |
|---|---|---|---|---|---|
| 90 | 0.01 | 0.06 | 0 | 0 | 1 |
| 90 | 0.06 | 0.06 | 11 | 0 | 0.8406 |
| 90 | 0.12 | 0.06 | 19 | 2 | 0.72 |
| 120 | 0.01 | 0.06 | 0 | 0 | 1 |
| 120 | 0.06 | 0.06 | 1 | 0 | 0.987 |
| 120 | 0.12 | 0.06 | 5 | 1 | 0.925 |
| 150 | 0.01 | 0.06 | 0 | 1 | 0.9892 |
| 150 | 0.06 | 0.06 | 1 | 3 | 0.9565 |
| 150 | 0.12 | 0.06 | 3 | 1 | 0.9583 |

Result SHA-256: `57503e1a21bcf538627c0fa1aa919cca2b6638403caabfc2b11101816249fb94`
