# GNIP Date Value Validation

status: completed

## Context

`GnipSearchAPI.set_dates()` already requires date filters to match the
documented `YYYY-MM-DD HH:MM` shape. Regex validation alone still accepts
impossible calendar values, such as invalid months or days, before deriving the
compact GNIP request payload dates.

## Completed Scope

- Added a shared API date filter helper that keeps the existing strict format
  check and validates the calendar value with `datetime.strptime`.
- Routed both start and end filter parsing through the helper before assigning
  `fromDate` and `toDate`.
- Extended the static baseline and docs so impossible date values remain
  rejected before live GNIP requests are built.

## Verification

- `scripts/check-baseline.py`
- `make check`
- `git diff --check`
