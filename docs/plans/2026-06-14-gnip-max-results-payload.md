# GNIP Max Results Payload

status: completed

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

## Verification Completed

- Seven focused query-payload tests passed on Python 3 and Python 2.
- All 34 tests passed on Python 3 and Python 2 through each of `make lint`,
  `make test`, `make build`, and `make check`.
- The absolute Makefile path passed from `/tmp`, proving location-independent
  execution after the new files were added.
- Six isolated mutations were rejected: omitted `maxResults`, removed page cap,
  added the field to count requests, bypassed the helper, removed the cap test,
  and removed project guidance.
- `git diff --check`, exact intended-path review, generated-artifact inventory,
  and credential-pattern scanning passed.
- Credentialed GNIP traffic and provider response data remained outside this
  offline change's scope.
