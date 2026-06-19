---
title: GNIP Response Shape
date: 2026-06-13
status: completed
execution: code
---

## Context

GNIP page bodies are bounded and decoded as JSON, but `parse_JSON` assumes the
decoded value is an object and that `results` is a list. Valid JSON arrays or
scalars can trigger incidental membership or indexing behavior, while a string
or object `results` value can be extended into unintended records.

## Priority

This is the highest-value remaining isolated provider-schema boundary because
every query page passes through the same parser before pagination, file output,
or use-case transforms. Explicit shape validation can fail through the existing
`QueryError` contract without changing credentials, requests, response limits,
pagination, or valid records.

## Prioritized Backlog

1. Require each decoded GNIP page to be an object.
2. Accept `results` only as a list, defaulting a missing key to an empty list.
3. Reuse the validated list for accumulation and optional file output.
4. Add Python 2/3 unit and hostile-mutation contracts plus repository guidance.
5. Keep per-record field schemas and use-case-specific validation separate.

## Implementation

- Add a small dependency-free response-shape helper and dedicated error.
- Route `parse_JSON` through the helper immediately after JSON decoding.
- Translate shape errors into the existing query failure type without exposing
  credentials or provider payloads.
- Extend tests, static checks, README, SECURITY, VISION, CHANGES, and AGENTS.

## Verification Plan

- Run focused shape tests, all offline tests, `scripts/check-baseline.py`, all
  four Make gates, Python 2/3 compilation and tests, workflow parsing,
  `git diff --check`, and intended-file artifact and secret scans.
- Remove the object guard, remove the results-list guard, and restore direct
  `tmp_response["results"]` file iteration; each hostile mutation must fail.
- Take one bounded exact-head push, pull-request, and code-scanning snapshot
  after push; do not poll.

## Work Completed

- Added a dependency-free response helper that requires an object page and a
  list `results` value, defaulting a missing key to an empty list.
- Routed accumulation and optional file output through the validated results
  list while preserving provider error and pagination behavior.
- Added Python 2/3 tests plus static, documentation, and completed-plan
  contracts.

## Verification Completed

- All 27 tests passed on Python 3 and Python 2.
- The focused four response-shape tests passed independently on both runtimes.
- All four Make gates passed.
- The object guard mutation failed after removing the dictionary check.
- The results-list guard mutation failed after removing the list check.
- The direct results iteration mutation failed after restoring
  `tmp_response["results"]` in file output.
- Python compilation, workflow parsing, `git diff --check`, and intended-file
  artifact and secret scans passed.
- The hosted push, pull-request, and code-scanning snapshot is a post-push
  evidence step; its bounded exact-head result is recorded after the
  implementation commit.
