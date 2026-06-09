# GNIP Sample Entrypoints

status: completed

## Context

`step1.py` and `step2.py` are executable GNIP samples, but they ran live search
requests as soon as the modules were imported. `step2.py` also opened the sample
CSV export during import. That made source inspection, future tests, and helper
reuse riskier because importing a script could require credentials or create a
local export.

## Completed Scope

- Moved sample execution in `step1.py` and `step2.py` into `main()` functions.
- Added `__main__` guards so imports do not perform live GNIP requests.
- Kept the sample query and CSV export behavior available when the scripts run
  directly.
- Extended `scripts/check-baseline.py` to reject sample scripts that move live
  GNIP calls or the CSV write back to import time.
- Updated README, VISION, and CHANGES with the entrypoint guardrail.

## Verification

- `make check`
- `git diff --check`
