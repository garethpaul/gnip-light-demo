---
title: GNIP Date Format Validation
date: 2026-06-09
status: completed
execution: code
---

## Context

`GnipSearchAPI.set_dates()` accepted start and end date filters with a regex
that used unescaped dots between date components. That allowed malformed
delimiters to pass before the compact GNIP API date strings were derived.

## Goals

- Require the documented `YYYY-MM-DD HH:MM` filter format.
- Match the full start and end strings before deriving API dates.
- Preserve the existing compact `YYYYMMDDHHMM` request payload format.
- Extend static verification and docs for the date parsing boundary.

## Implementation

- Added an anchored `DATE_RE` for `YYYY-MM-DD HH:MM` values.
- Switched start and end parsing to `DATE_RE.match`.
- Built `fromDate` and `toDate` from captured date components.
- Updated `scripts/check-baseline.py`, README, SECURITY, VISION, and CHANGES.

## Verification

- `scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
