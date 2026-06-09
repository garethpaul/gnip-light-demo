# GNIP Timeout Validation

status: completed

## Context

GNIP live requests use `GNIP_REQUEST_TIMEOUT` to let maintainers tune slow API
paths. The previous configuration parsed the environment variable directly with
`int()`, which produced a generic import-time error for invalid text and allowed
non-positive timeout values.

## Completed Scope

- Added a timeout validation helper with the existing 30-second default.
- Rejected non-integer and non-positive timeout overrides with a clear error.
- Kept the `requests` call using the validated `REQUEST_TIMEOUT` value.
- Extended the static baseline and docs to preserve the request configuration
  guardrail.

## Verification

- `make check`
- `git diff --check`
