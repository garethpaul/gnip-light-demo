# GNIP Timeout Exception Handling

status: completed

## Context

GNIP requests already use an explicit `GNIP_REQUEST_TIMEOUT` value, but a slow
upstream call can still raise a `requests` timeout exception. The sample should
report that failure consistently instead of exposing a traceback or continuing
toward result parsing.

## Completed Scope

- Added an explicit `requests.exceptions.Timeout` handler to the GNIP request
  path.
- Extended `scripts/check-baseline.py` so the timeout handler remains before
  connection error handling and result parsing.
- Documented the timeout exception behavior in README, VISION, SECURITY, and
  CHANGES.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
