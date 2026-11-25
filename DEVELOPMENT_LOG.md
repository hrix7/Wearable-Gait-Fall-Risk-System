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

## 2026-11-15

Expose interval sample size and separate sample-SD variability.

Adds interval_count and sample_interval_cv_percent (sample SD, ddof=1), undefined with fewer than two intervals. Existing interval_cv_percent retains population SD, ddof=0, so historical semantics are preserved. The sample-CV ratio is not claimed to be an unbiased estimator or a clinical fall-risk score.

Validation before publication: full unittest suite, pipeline regeneration/byte verifier, diff review and existing workflow-policy tests. Workflows and permissions unchanged. Hosted validation is followed after publication.

## 2026-11-17 — Flattened-signal gap scenarios

Completed the retained, unpublished implementation from November 16. Added nine deterministic finite flattening scenarios: replace [0.4T,0.5T) by 1 g while retaining timestamps. Evaluate separately against nominal events and reference centers outside the gap. This is not support for real NaN/missing samples, participant gait, or clinical fall-risk prediction. Full-precision masked signal hashes reproduce from the generator/config, not the rounded base CSV. Tests cover mask boundaries, invalid intervals, reference accounting and exact regeneration. Full unit tests, pipeline regeneration and artifact verification run before publication; no workflow or permission changes.

## 2026-11-18 — Paired additive motion-burst scenarios

Nine motion conditions add a fixed 0.4 g, 2.7 Hz sinusoid under a sin-squared envelope on [0.3T,0.6T). Original pulse centers and paired noise are unchanged. Both predeclared detectors are scored against independent event truth. Tests check analytic envelope samples, exact untouched boundaries, invalid inputs, full-precision signal hashes and independently recomputed metrics. This is a teaching acceleration surrogate, not measured participant motion or clinical fall-risk validation. Full suite: 33 tests passed; pipeline generation, independent --verify and diff checks passed before publication. No workflow/permission changes; workflow policy tests passed.

## 2026-11-19 — Independent noise-realization sensitivity

Added ten predeclared noise seeds per cadence/noise cell with fixed regular event times and detector. Reports each replicate hash/metrics plus descriptive F1 min/mean/max and defined-value count. This measures within-cell noise-only sensitivity, not population uncertainty, confidence intervals or clinical fall risk. Realizations are paired across cells and must not be pooled as independent samples. Original benchmark seeds/results remain separate. Tests independently reconstruct each signal/metric, verify seed-invariant zero-noise output and validate seed specifications. Full suite: 36 tests passed; pipeline generation, independent --verify and diff checks passed before publication. No workflow or permission changes; workflow policy tests passed.

## 2026-11-20 — Paired motion effects over noise realizations

Each predeclared noise realization now applies the same fixed motion burst to its own base signal, preserving independent event truth. Reports motion signal hashes/F1 and original-minus-motion paired F1 min/mean/max, including negative differences when motion happens to improve scores. These are descriptive noise-only pairs, not confidence intervals or subject-population claims. Tests reconstruct hashes/scores and use identity perturbations to prove exactly zero paired effect. Full suite: 38 tests passed; pipeline generation, independent --verify and diff checks passed before publication. Workflow policy tests passed without workflow/permission changes.

## 2026-11-21 — Evaluate paired flattened gaps across noise realizations

Each existing noise replicate now exports independently reproducible gap-signal hash and both nominal-reference and present-reference metrics/counts. Original and motion conditions retained. Reconstruct gaps via independent sample assignment and recompute both event populations. Descriptive synthetic scenario results, not missing-value handling or population uncertainty.

Validation: full existing suite plus new tests (39 passed), pipeline generation and independent --verify, scoped diff review and git diff --check before publication. Hosted CI is followed after pushing. Existing read-only validation/publisher workflows unchanged; workflow-policy tests included.

## 2026-11-24 — Paired gap-effect summaries

Summarize original-minus-flattened-gap F1 within each noise cell for nominal and present reference populations separately. Export defined pair count, mean and extrema; retain negative effects and null when no pairs are defined. Hand fixtures independently verify sign, reference separation and undefined behavior. Finite descriptive synthetic scenarios, not subject-population uncertainty.

Validation before publication: 41 full-suite tests passed, pipeline regeneration and independent --verify passed, scoped diff/checksum review and git diff --check passed. Workflow policy tests included; workflows and permissions unchanged. Hosted validation followed after pushing.

## 2026-11-25 — Independent baseline on paired flattened gaps

Run the existing fixed-height baseline on each paired noise realization after the same flattening. Report nominal and present-reference event metrics using identical baseline detections. Independently reconstruct each signal/detection/reference population; retain original prominence outputs. No tuning, real missing-value handling or clinical fall prediction.

Pre-publication validation: 43 full-suite tests passed; pipeline generation and independent --verify, scoped diff and checksum review, git diff --check passed. Existing workflow policy tests included; no permission/workflow changes. Hosted CI followed after publication.
