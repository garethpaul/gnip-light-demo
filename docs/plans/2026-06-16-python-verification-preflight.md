# Python Verification Preflight

status: completed

## Context

The maintained Python 3 checker launches its own tests through
`sys.executable`, but `Makefile` hard-codes the initial `python3` command.
Contributors cannot select another compatible interpreter, and a missing or
incompatible command fails without a repository-owned diagnostic.

The live GNIP client remains Python 2.7 code for retired APIs. This plan changes
only the offline verification entry point and does not claim live-client or API
modernization.

## Prioritized Engineering Tasks

1. Make the offline verification entry point explicit, configurable, and
   fail-fast while preserving the checker's `sys.executable` test ownership.
2. Plan a replacement for retired GNIP/Twitter APIs only with an available
   service contract, credentials, fixtures, and migration target.
3. Migrate the Python 2.7 live client only after the replacement API and CSV
   compatibility requirements are authoritative.

This plan implements item 1 because it affects every maintained gate and is
fully verifiable without credentials or a live request.

## Objectives

- Define one Make-level Python command with a `python3` default.
- Add a POSIX preflight that rejects missing and non-Python-3 commands with
  actionable diagnostics.
- Launch the baseline checker through the selected interpreter and retain its
  existing `sys.executable` ownership for all 34 tests.
- Document the supported override and distinguish offline Python 3 verification
  from the unchanged Python 2.7 live-client boundary.
- Add static and behavioral contracts for propagation, preflight behavior,
  checker ownership, documentation, and completed evidence.

## Scope

- Update `Makefile`, `scripts/check-baseline.py`, `README.md`, `AGENTS.md`,
  `VISION.md`, and `CHANGES.md`.
- Add a small POSIX-shell preflight helper and complete this plan with evidence.
- Do not change live-client Python, dependencies, CSV output, API requests,
  credentials, fixtures, hosted permissions, or workflow matrices.

## Verification

- Run POSIX shell syntax and Python compilation checks.
- Run all four Make aliases from the repository root.
- Run `make check` from an external working directory.
- Run the gate through an explicit compatible Python command override.
- Prove missing and non-Python-3 commands fail with intended diagnostics.
- Confirm the full 34-test suite uses the selected checker interpreter.
- Reject isolated hostile mutations covering propagation, preflight behavior,
  checker ownership, documentation, and completed-plan evidence.
- Audit exact paths, generated caches, credential-like values, dependency and
  workflow drift, conflict markers, file modes, and whitespace.

## Runtime Boundary

No GNIP/Twitter credential, live request, pagination response, CSV export,
retrieved payload, browser route, or production integration is executed or
claimed. Python 2.7 live-client compatibility remains unchanged.

## Verification Completed

- All 34 tests passed through the selected Python 3.12.8 checker interpreter
  and through the additive Python 2.7.18 compatibility run.
- All four Make gates passed: `make check`, `make lint`, `make test`, and
  `make build`.
- The absolute Makefile path passed from `/tmp`.
- An explicit Python override passed and retained checker-owned unit discovery.
- The missing-command case failed with the intended diagnostic.
- The non-Python-3 case failed with the intended diagnostic.
- Nine isolated mutations were rejected across Make defaults and propagation,
  checker selection, command lookup, major-version enforcement, diagnostics,
  documentation, plan status, and checker-owned unit discovery.
- The generated-artifact inventory was empty.
- The credential-pattern scan passed.
- `sh -n` and direct Python source compilation passed before the full gates.
