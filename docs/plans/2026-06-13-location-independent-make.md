---
title: Location-Independent GNIP Verification
date: 2026-06-13
status: completed
execution: code
---

## Context

The maintained GNIP baseline passes from the checkout but fails when the
absolute Makefile is invoked from another working directory because the
checker path is resolved relative to the caller.

## Priority

This is the next isolated reliability gap because automation should be able to
load the repository Makefile without first changing directories. The checker
already roots all Python 2/3 compilation and unittest execution internally, so
the implementation should remain confined to the Make entry point and its
static contract.

## Requirements

- Derive the repository root from `MAKEFILE_LIST`.
- Preserve spaces in the loaded Makefile path before Make list functions select
  the final file.
- Invoke `scripts/check-baseline.py` through its repository-rooted path.
- Add static contracts for the rooted Makefile, completed plan, external-run
  evidence, and synchronized guidance.
- Add mutation-sensitive verification for root derivation, checker execution,
  plan status/evidence, and documentation drift.
- Preserve production modules, tests, dependencies, workflows, and credential
  handling unchanged.

## Verification Plan

- Run all offline tests and `scripts/check-baseline.py` on Python 3 and Python
  2 through all four Make gates at repository root.
- Run all four Make gates from /tmp through the absolute Makefile path.
- Run the full gate through an absolute Makefile path inside a spaced checkout.
- Reject isolated root-derivation, checker-command, plan-status, plan-evidence,
  and documentation mutations.
- Run workflow parsing, `git diff --check`, exact-path review, secret scanning,
  and bytecode/generated-artifact checks.

## Non-Goals

- Changing GNIP requests, credentials, timeouts, pagination, response parsing,
  timestamp handling, exports, dependencies, or workflow policy.
- Claiming live GNIP API requests, retrieved payloads, pagination, or exports
  without credentials.

## Work Completed

- Derived the repository root from the loaded Makefile and invoked the existing
  checker through its absolute repository path.
- Protected spaces with a sentinel while selecting and resolving the loaded
  Makefile, then restored them in the final repository root.
- Extended the baseline with rooted-Makefile, completed-plan, external-run, and
  synchronized-guidance contracts.
- Preserved production modules, tests, dependencies, workflows, credential
  handling, and generated-artifact policy unchanged.

## Verification Completed

- All 27 tests passed on Python 3 and Python 2.
- All four Make gates (`make lint`, `make test`, `make build`, and `make check`)
  passed at repository root and from /tmp through the absolute Makefile path.
- The current 56-test full gate passed from an external directory through an
  absolute Makefile path inside a spaced checkout on GNU Make 4.2 and 4.4.
- The root-derivation mutation failed.
- The checker-command mutation failed.
- The plan-status mutation failed.
- The plan-evidence mutation failed.
- The documentation mutation failed.
- Workflow parsing, `git diff --check`, exact intended-path review, added-line
  secret scanning, and bytecode/generated-artifact inspection passed.
- Live GNIP API requests, pagination responses, retrieved payloads, and exports
  were unavailable without credentials and are not claimed.
