---
title: GNIP Failure Exit Status
date: 2026-06-16
status: completed
execution: code
---

## Context

Seven invalid-input and request-failure branches print an error and then call
bare `sys.exit()`. Python treats that as a successful status, so shell scripts
and schedulers can report invalid dates, invalid count buckets, timeouts,
connection failures, HTTP failures, or oversized responses as successful runs.
The separate query-preview path intentionally exits successfully after printing
a redacted payload and must retain that behavior.

## Priority

This is the highest-value remaining deterministic CLI contract because it can
silently invert failure reporting for every live request without requiring a
provider credential or successor API to reproduce.

## Plan

1. Change only the seven genuine error branches to `sys.exit(1)`.
2. Preserve the one intentional query-preview `sys.exit()` success path.
3. Add a dependency-free source contract and baseline enforcement for the
   exact failure/success split.
4. Update repository guidance and completed verification evidence.
5. Run focused and full tests, all Make gates, external-directory validation,
   isolated mutations, and final diff/artifact/secret audits.
6. Push the exact branch, open a stacked pull request against the Python
   preflight branch, and take one bounded hosted/security snapshot.

## Non-Goals

- Exercising retired GNIP/Twitter endpoints or adding credentials.
- Changing error messages, response parsing, pagination, or query payloads.
- Changing the successful query-preview behavior.
- Migrating the live Python 2.7 client.

## Verification Required

- The focused exit-status test and complete dependency-free suite pass.
- `make check`, `make lint`, `make test`, and `make build` pass from the
  repository, and the absolute Makefile check passes externally.
- Mutations restoring a successful failure exit, making preview nonzero,
  removing the focused contract, or staling plan evidence fail.
- Python 2 production syntax and final diff/artifact/credential audits pass.

## Work Completed

- Changed the seven invalid-input and request-failure branches to `sys.exit(1)`.
- Preserved the one bare successful exit used by redacted query-preview mode.
- Added a Python 2/3-compatible dependency-free source contract and baseline,
  guidance, changelog, and completed-plan enforcement.

## Verification Completed

- The focused exit-status test passed on Python 3 and Python 2.
- The complete suite passed on Python 3 and Python 2 with 35 tests per runtime.
- All four Make gates passed in the isolated baseline mirror and final worktree.
- The external-directory Make gate passed through the absolute Makefile path.
- The successful-failure-exit mutation failed after restoring one bare exit in
  an error branch.
- The nonzero-preview-exit mutation failed after making the intentional preview
  path exit with status 1.
- The focused-test contract mutation failed after renaming the behavior test.
- The plan-status mutation failed after restoring an active status.
- The plan-evidence mutation failed after removing the failure-exit mutation
  result.
- Python 2 production syntax, diff, generated-artifact, credential,
  conflict-marker, file-mode, and exact-upstream audits completed before commit.
