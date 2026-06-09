# Changes

## 2026-06-09

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
