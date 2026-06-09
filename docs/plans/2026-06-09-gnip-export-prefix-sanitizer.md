# GNIP Export Prefix Sanitizer

status: completed

## Context

Paged GNIP exports derive their JSON filename prefix from the query text. The
previous munger replaced a few punctuation characters but left other path or
control characters untouched, which made output filenames harder to reason
about when a query contained unusual text.

## Completed Scope

- Added `safe_file_name_prefix()` to normalize query-derived prefixes to a
  conservative filename character set.
- Avoided empty or dot-only prefixes by falling back to `query`.
- Extended the static baseline and docs so export filename normalization remains
  visible.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
