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

## Flattened-signal gap probe

A separate finite dropout surrogate replaces [0.4T,0.5T) with 1 g. Nominal-reference misses include intentionally masked pulse centers; present-reference misses exclude them. This does not validate handling of real missing values. Reproduce from the regular generator and stated mask.

| Cadence | Noise SD | Reference centers in gap | Nominal FN | Present FN | Present FP |
|---|---|---|---|---|---|
| 90 | 0.01 | 3 | 3 | 0 | 0 |
| 90 | 0.06 | 3 | 3 | 0 | 9 |
| 90 | 0.12 | 3 | 6 | 3 | 22 |
| 120 | 0.01 | 4 | 4 | 0 | 0 |
| 120 | 0.06 | 4 | 4 | 0 | 1 |
| 120 | 0.12 | 4 | 8 | 4 | 6 |
| 150 | 0.01 | 5 | 5 | 0 | 0 |
| 150 | 0.06 | 5 | 4 | 0 | 2 |
| 150 | 0.12 | 5 | 6 | 2 | 5 |

## Additive motion-burst probe

Independent additive 0.4 g, 2.7 Hz sinusoid under a sin-squared envelope on [0.3T,0.6T). Event truth and paired base noise remain unchanged. Teaching perturbation, not participant motion validation.

| Cadence | Noise SD | Extra | Missed | Prominence F1 | Fixed-height F1 |
|---|---|---|---|---|---|
| 90 | 0.01 | 6 | 2 | 0.871 | 0.871 |
| 90 | 0.06 | 13 | 1 | 0.8 | 0.8125 |
| 90 | 0.12 | 24 | 5 | 0.6234 | 0.6154 |
| 120 | 0.01 | 5 | 3 | 0.8974 | 0.8974 |
| 120 | 0.06 | 7 | 3 | 0.875 | 0.9 |
| 120 | 0.12 | 9 | 5 | 0.825 | 0.6591 |
| 150 | 0.01 | 2 | 2 | 0.9574 | 0.9574 |
| 150 | 0.06 | 4 | 3 | 0.9263 | 0.9474 |
| 150 | 0.12 | 7 | 6 | 0.8632 | 0.866 |

## Independent noise realizations

Ten predeclared noise seeds per fixed cadence/noise cell; same analytic event times and detector. Descriptive noise-only F1 range/mean, not a confidence interval or subject variability. Noise realizations are paired across cells.

| Cadence | Noise SD | Defined F1 replicates | Mean F1 | Min F1 | Max F1 |
|---|---|---|---|---|---|
| 90 | 0.01 | 10 | 1 | 1 | 1 |
| 90 | 0.06 | 10 | 0.8461 | 0.8056 | 0.8923 |
| 90 | 0.12 | 10 | 0.7085 | 0.6234 | 0.7532 |
| 120 | 0.01 | 10 | 1 | 1 | 1 |
| 120 | 0.06 | 10 | 0.9795 | 0.962 | 1 |
| 120 | 0.12 | 10 | 0.9227 | 0.8642 | 0.962 |
| 150 | 0.01 | 10 | 1 | 1 | 1 |
| 150 | 0.06 | 10 | 0.9802 | 0.9691 | 0.9895 |
| 150 | 0.12 | 10 | 0.9465 | 0.8817 | 0.9792 |

Result SHA-256: `4bf5f438f8ae4fa36f7276a63db4a9086e07326de3b6a69d0e86bde95accfd0a`
