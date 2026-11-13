# Development backlog

## Completed — 2026-11-12

- Added a deterministic, nine-condition synthetic gait event benchmark, independent reference events, one-to-one evaluation and reproducible reports.
- Added detector/summary input validation, exact minimum-sample spacing and regression tests.
- Added pinned dependencies and read-only GitHub Actions validation with daily report artifacts.

## Next

1. Add timing jitter, missing segments and sensor-artifact scenarios without tuning on the evaluation grid.
2. Add a separate detector baseline and compare matched-event/cadence errors.
3. Add independent seeds and uncertainty summaries with a stated sampling model.
4. Review public gait dataset terms and subject-wise validation before any real-world claims.

- Completed 2026-11-13: Independent fixed-height step baseline with event-error comparison.
