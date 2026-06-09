# GNIP Endpoint Validation

status: completed

## Context

The wrapper failed fast when GNIP environment variables were missing, but it did
not validate that `GNIP_SEARCH_ENDPOINT` was a usable HTTPS endpoint before
building the API client.

## Completed Scope

- Trimmed environment variable values before accepting them.
- Added `required_https_endpoint` for `GNIP_SEARCH_ENDPOINT`.
- Required the endpoint to use the `https` scheme and include a host.
- Extended the static baseline, README, VISION, and CHANGES.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
