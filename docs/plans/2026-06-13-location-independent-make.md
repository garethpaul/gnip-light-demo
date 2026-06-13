---
title: Location-Independent GNIP Verification
date: 2026-06-13
status: planned
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

Pending implementation.

## Verification Completed

Pending implementation and validation. Run `make check` before completion.
