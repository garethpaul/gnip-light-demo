# Changes

## 2026-06-13

- Replaced character-set trimming of GNIP geo-export timestamps with exact
  `.000Z` suffix removal so seconds ending in zero remain intact.
- Redacted query text and pagination tokens from query-preview and no-result
  output and kept printable query errors from exposing request or provider
  response payloads.

## 2026-06-12

- Pinned the Twitter Ads SDK VCS dependency to the reviewed upstream `master`
  commit instead of resolving a mutable branch.
- Streamed GNIP page bodies through a 16 MiB decompressed-size boundary and
  closed responses and sessions on success and failure paths.
- Added a dependency-free GNIP link literal parser that rejects expressions,
  mappings, scalars, empty collections, and non-string link values before
  aggregation.
- Counted malformed link fields as `InvalidLinks` and added focused Python 2/3
  regression tests for accepted and rejected literal shapes.
- Bounded serialized link fields, collection cardinality, and individual link
  lengths before literal parsing and aggregation.
- Removed unconditional query-payload and link-value debug output from live
  result processing.

## 2026-06-10

- Bounded paged GNIP searches to 1,000 pages and rejected blank, non-string, or
  repeated continuation tokens before another authenticated request.
- Made the timeframe helper importable on Python 3 and run its behavior tests
  in a pinned Python 3.10/3.12/3.14 GitHub Actions matrix.
- Kept full Python 2 syntax and unit checks additive when Python 2 is available.

## 2026-06-09

- Rejected impossible calendar values in GNIP date filters before compact API
  request dates are derived.
- Tightened GNIP date filters to the documented `YYYY-MM-DD HH:MM` format before
  API date strings are derived.
- Handled GNIP request timeout exceptions with a clear error before result
  parsing.
- Added `make lint`, `make test`, and `make build` aliases so local verification
  has the expected pre-push gate targets in addition to `make check`.
- Normalized paged GNIP output filename prefixes to a conservative filename
  character set before JSON exports are written.
- Moved live sample scripts behind main guards and added a baseline check so
  imports do not trigger GNIP requests or CSV writes.

## 2026-06-08

- Added `make check` for static legacy GNIP demo verification.
- Replaced dynamic `exec` link parsing with `ast.literal_eval`.
- Switched editable git dependencies from `git://` to HTTPS transport.
- Fixed `Timeframe.days` after inverted date fallback and covered it with a unit test.
- Added fail-fast GNIP credential validation, request timeouts, and HTTP error handling.
- Required `GNIP_SEARCH_ENDPOINT` to parse as an HTTPS URL with a host.
- Rejected embedded credentials, query strings, or fragments in
  `GNIP_SEARCH_ENDPOINT`.
- Required `GNIP_REQUEST_TIMEOUT` overrides to be positive integers.
- Rejected generated Python bytecode artifacts during baseline verification and
  disabled bytecode writes for Python 2 unit discovery.
- Documented required GNIP credential environment variables and ignored local exports.
