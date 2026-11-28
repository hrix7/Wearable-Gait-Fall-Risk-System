# Development backlog

## Completed — 2026-11-12

- Added a deterministic, nine-condition synthetic gait event benchmark, independent reference events, one-to-one evaluation and reproducible reports.
- Added detector/summary input validation, exact minimum-sample spacing and regression tests.
- Added pinned dependencies and read-only GitHub Actions validation with daily report artifacts.

## Completed — 2026-11-13

Independent fixed-height event-detector baseline.

## Completed — 2026-11-14

Bounded event-time jitter with independent timing/noise channels.

## Completed — 2026-11-15

Expose interval sample size and separate sample-SD variability.

## Completed — 2026-11-17

Flattened-signal gap scenarios.

## Completed — 2026-11-18

Paired additive motion-burst scenarios.

## Completed — 2026-11-19

Independent noise-realization sensitivity.

## Completed — 2026-11-20

Paired motion effects over noise realizations.

## Next priorities

1. Compare flattened-gap effects over paired noise realizations with explicit reference populations.
2. Add independently checked summary uncertainty without subject-population claims.
3. Review public gait dataset terms and subject-wise evaluation.

## Completed — 2026-11-21

Evaluate paired flattened gaps across noise realizations.

## Completed — 2026-11-24

Paired gap-effect summaries.

## Current ordered next steps

1. Compare a distinct detector baseline under the same paired gap conditions; keep real missing-value handling separate.
2. Review public-data terms, exact release/checksums and subject mappings before ingestion; keep synthetic and public-data evaluation distinct.

## Completed — 2026-11-25

Independent baseline on paired flattened gaps.

## Current next steps

1. Compare paired baseline error differences without treating noise seeds as independent human participants.
2. Review real-data license/version/checksums and subject mappings before ingestion.

## Completed — 2026-11-26

Validate paired gap-summary inputs.

## Current ordered next steps

1. Compare paired baseline error differences over the existing noise-only scenario grid.
2. Review official data terms/version/checksums and subject mapping before any real-data ingestion.


## Completed — 2026-11-28

Paired detector comparison. Prominence-minus-fixed-height F1 on identical flattened-gap noise realizations, separately against nominal/present reference events; signed descriptive ranges, direction counts and defined-pair counts. Noise seeds are not human participants; no population interval or detector selection.

## Next ordered work

1. Review these conditional diagnostics before expanding experiments; keep descriptive scenarios separate from statistical uncertainty.
2. Review exact public release/terms/checksums and participant mapping before real-data integration.
