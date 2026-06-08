# GNIP Light Demo Baseline Plan

status: completed

## Context

`gnip-light-demo` is a legacy Python 2 GNIP/Twitter full-archive search sample.
The repository relies on local GNIP credentials and old editable VCS
dependencies, so local verification needs static checks that do not perform live
API calls.

## Objectives

- Add a reproducible `make check` command that does not require GNIP credentials.
- Keep GNIP credentials sourced from local environment variables.
- Remove dynamic execution of API-supplied link data.
- Use authenticated HTTPS transport for editable git dependencies.
- Keep generated tweet exports and local environment files out of git.
- Cover timeframe parsing and inverted-date fallback with a local unit test.
- Fail fast when GNIP credentials are missing or HTTP requests fail.
- Add an explicit timeout for GNIP API requests.

## Work Items

1. Added `Makefile` and `scripts/check-baseline.py`.
2. Replaced `exec` link parsing with `ast.literal_eval`.
3. Switched editable git dependencies from `git://` to `git+https://`.
4. Added `.gitignore` entries for Python caches, local env files, and sample exports.
5. Fixed `Timeframe.days` after invalid date fallback and added a regression test.
6. Added clear missing-credential validation, request timeouts, and HTTP error handling.
7. Updated README, VISION, and CHANGES with the baseline.

## Verification

- `make check`
- `python2 -m unittest discover -s tests`
- `git diff --check`
