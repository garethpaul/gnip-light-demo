# GNIP Max Results Payload

status: planned

## Context

`FullArchiveSearch.query_count` reaches `GnipSearchAPI.query_api` as
`max_results`, but request construction currently drops the value. A caller can
therefore request a smaller page and still receive the provider default, while
the sample's larger request is silently ignored.

## Scope

- Add a dependency-free Python 2/3 helper for constructing the base GNIP rule
  payload.
- Include `maxResults` for activity searches, validate positive integer-like
  input, and cap a single request at the provider's 500-result page boundary.
- Preserve the existing 500-result paged-search override.
- Keep count/timeline requests free of the activity-only `maxResults` field.
- Add focused unit and static mutation-sensitive contracts, then update the
  repository guidance and changelog.

## Non-Goals

- Do not change the existing pagination continuation or 1,000-page ceiling.
- Do not implement a total-result stopping policy for `query_count`.
- Do not issue credentialed GNIP requests or record provider data.

## Verification Plan

- Run the focused query-payload tests on every available Python 3 and Python 2
  interpreter path.
- Run `make check` from the repository root and through the absolute Makefile
  path from an external directory.
- Confirm hostile mutations that omit `maxResults`, remove validation, remove
  the 500-result cap, add the field to count requests, or bypass the helper are
  rejected.
- Run diff, generated-artifact, and added-line secret audits before committing.
