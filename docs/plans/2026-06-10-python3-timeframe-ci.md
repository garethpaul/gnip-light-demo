# Python 3 Timeframe CI

status: completed

## Context

The repository remains a Python 2-era GNIP client, but its dependency-free
timeframe helper and tests are portable except for one script-only print
statement. The existing baseline skipped all behavior tests when Python 2 was
unavailable, which made modern hosted validation static-only.

## Changes

- Made the timeframe module's script output valid on Python 2 and Python 3.
- Run dependency-free timeframe tests on Python 3 in every baseline execution.
- Preserve the optional full Python 2 syntax and unit-test pass when a Python 2
  interpreter is available.
- Added pinned, least-privilege Python 3.10, 3.12, and 3.14 GitHub Actions jobs
  without installing the legacy VCS dependency graph or using GNIP credentials.

## Verification

- `make check`
- Workflow YAML parse
- Hosted Python 3.10, 3.12, and 3.14 jobs
