---
title: Exact GNIP Posted-Time Suffix Removal
date: 2026-06-13
status: planned
execution: code
---

## Context

Geo exports currently call `postedTime.strip(".000Z")`. Python `strip` treats
that argument as a set of characters, not an exact suffix, so a valid GNIP
timestamp ending in `:10.000Z` becomes `:1` and one ending in `:00.000Z` loses
both seconds digits. The exported timestamp is silently corrupted before it is
returned to callers.

## Priority

This is the highest-value remaining isolated data-integrity defect because it
changes valid provider values without raising and affects every geo export whose
seconds end in zero. Exact suffix handling can fix the corruption without live
credentials, API calls, or changes to query construction.

## Prioritized Backlog

1. Remove only the exact `.000Z` suffix from GNIP posted-time strings.
2. Preserve seconds digits and leave values without that suffix unchanged.
3. Route geo export timestamps through the helper and reject restoration of
   character-set stripping.
4. Add Python 2/3 behavior tests, static/mutation contracts, and repository
   guidance.
5. Keep broader timestamp parsing, timezone normalization, and provider schema
   validation separate.

## Implementation

- Add a dependency-free `gnip_search.timestamps` helper with Python 2/3 string
  compatibility.
- Replace the geo export `.strip(".000Z")` call with the exact helper.
- Add unit coverage for zero-ending seconds, ordinary seconds, absent suffixes,
  and invalid value types.
- Extend the baseline and README, SECURITY, VISION, CHANGES, and AGENTS guidance.

## Verification Plan

- Run focused timestamp tests, all offline tests, `scripts/check-baseline.py`,
  `make lint`, `make test`, `make build`, and `make check`, Python 2/3 syntax
  and behavior gates, workflow parsing, diff checks, and intended-file
  secret/artifact scans.
- Restore character-set stripping, remove the exact suffix guard, and remove the
  timestamp tests; each hostile mutation must fail.
- Take one bounded exact-head push, pull-request, and CodeQL snapshot after
  push; do not poll.

## Work Completed

- Pending implementation.

## Verification Completed

- Pending implementation and verification.
