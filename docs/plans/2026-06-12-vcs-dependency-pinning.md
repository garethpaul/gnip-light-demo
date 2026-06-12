---
title: GNIP VCS Dependency Pinning
date: 2026-06-12
status: completed
execution: code
---

# GNIP VCS Dependency Pinning

## Summary

Replace the floating Twitter Ads SDK source reference with the exact commit
currently selected by the upstream default branch.

## Requirements

- Preserve HTTPS transport and editable-install syntax required by the legacy
  sample.
- Pin both VCS dependencies to full 40-character commit SHAs.
- Keep hosted verification offline and dependency-free.
- Do not claim that source pinning modernizes Python 2, authenticates artifacts,
  or proves compatibility with retired GNIP services.

## Verification

- `git ls-remote --symref` resolved the upstream `master` commit to
  `a3dd5819341e77aa469d0b4b3399f0bcd028c80c`.
- The exact commit's package metadata was inspected without executing setup
  hooks.
- Python 2 and Python 3 offline gates passed with all 17 tests.
- Requirements drift, a shortened SHA, a floating branch, incomplete evidence,
  and missing guidance hostile mutations were rejected.
- `git diff --check` and Python compilation passed.
