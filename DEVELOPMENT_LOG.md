# Development log

## 2026-11-12 — reproducible gait event benchmark

Added nine fixed synthetic cadence/noise conditions with known event centers, independent of detector output. Ordered one-to-one matching maximizes true positives before minimizing timing error; no detection can count twice. Reports include false positives, false negatives, F1, timing MAE and cadence error. Detector inputs and summary indices now reject invalid/nonfinite values. Minimum detection spacing uses the ceiling in samples so it cannot round below the requested physical interval.

Local validation: Python 3.11.0; 17 tests, deterministic export, independent recomputation, artifact tamper rejection, diff whitespace check and actionlint 1.7.12. Pinned numpy 2.2.6, pandas 2.3.2 and scipy 1.16.2 match the installed runtime. Shellcheck is not available locally. Hosted validation is linked from the repository Actions page and is checked after publication.

No participant data, clinical fall-risk model or completed multimodal device validation is implied. The existing academic IMU/FSR/PPG concept remains distinct from this new synthetic acceleration-only benchmark.

## 2026-11-13

Independent fixed-height step baseline with event-error comparison.

Adds a predeclared 0.125 g threshold above record median, local maxima and chronological refractory selection. It does not call the main SciPy prominence detector, and its thresholds are not selected on this evaluation grid. Both detectors use the same minimum interval and analytic references; results include baseline event FP/FN/F1 for every existing condition. A baseline is not clinical validation.

Validation: full unittest suite, pipeline regeneration and byte-for-byte verifier, diff review; GitHub validation outcome is tracked after push. No workflow/permission changes.

## 2026-11-14

Bounded event-time jitter with independent timing/noise channels.

Adds nine stress cases with independently seeded uniform timing offsets, half-width min(0.06 s, 0.2 periods), plus full jitter_data.csv and fingerprints. Actual perturbed centers define event truth; nominal cadence remains a generator setting. Both detectors are evaluated without tuning; the original nine regular-timing cases are retained.

Validation before publication: full unittest suite, regenerated pipeline artifacts, byte-for-byte verification and diff review. Workflow configuration/permissions unchanged; existing policy tests pass. Hosted CI is followed after the tested source is published.
