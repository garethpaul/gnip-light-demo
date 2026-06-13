# GNIP Diagnostic Redaction

status: completed

## Context

The repository documents that query payloads and retrieved provider content are
not logged, but query-preview mode still prints the full rule payload and
`QueryError.__str__` includes both the request payload and provider response.
Callers print these exceptions, so search terms, pagination tokens, or retrieved
content can reach stderr despite the existing static check.

## Scope

1. Add a dependency-free Python 2/3 helper that copies rule payloads and masks
   query text plus pagination tokens while retaining non-sensitive shape fields.
2. Use the redacted copy in query-preview output.
3. Keep `QueryError` payload and response attributes for compatibility, but make
   its printable representation message-only.
4. Add behavior tests and strengthen the baseline against both current leak
   syntaxes, helper removal, and test removal.
5. Synchronize README, SECURITY, VISION, and CHANGES.

## Verification Plan

- Run focused privacy tests, full Python 3 and Python 2 test discovery, all four
  Make gates, compilation, workflow parsing, diff checks, and secret scans.
- Restore raw preview printing, restore exception payload formatting, remove the
  redaction helper, and remove its tests; each hostile mutation must fail.
- Push a stacked pull request and record one bounded exact-head workflow, check,
  and CodeQL snapshot without polling.

## Risk And Rollback

The change affects diagnostics only. Query execution and exception attributes
remain intact. Rollback restores the old printable diagnostics; no API request,
stored data, credential, or export format changes.

## Work Completed

- Added a dependency-free redaction helper that copies rule payloads and masks
  query text plus pagination tokens.
- Routed query-preview output through the redacted copy while preserving dates,
  buckets, and other non-sensitive diagnostic fields.
- Removed the full rule payload from paged no-result diagnostics.
- Kept `QueryError.payload` and `QueryError.response` available to callers while
  making the printable exception representation message-only.
- Replaced provider-controlled error text with a fixed printable query failure
  message while retaining the full response attribute for inspection.
- Added Python 2/3 behavior coverage and synchronized the baseline and project
  guidance.

## Verification Completed

- Focused privacy tests passed on Python 3 and Python 2.
- The raw preview mutation failed with the query-payload logging contract.
- The no-result payload mutation failed with the query-payload logging contract.
- The exception payload mutation failed with the diagnostic exposure contract.
- The provider error-message mutation failed with the fixed-message contract.
- The redaction helper removal mutation failed with the helper contract.
- The redaction test removal mutation failed with the behavior-coverage
  contract.
- All 19 tests passed on Python 3 and Python 2.
- `scripts/check-baseline.py` and all four Make gates passed.
- Python 2 compilation passed for the legacy runtime and tests; Python 3
  compilation passed for the documented dual-runtime modules, tests, and
  checker.
- The hosted pull-request and CodeQL snapshot is recorded separately after push;
  this plan claims only the completed pre-push verification above.
