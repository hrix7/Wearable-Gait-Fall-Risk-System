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
