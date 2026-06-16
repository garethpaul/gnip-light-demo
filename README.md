# gnip-light-demo

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/gnip-light-demo` is a Python project. The checked-in files describe a Python project with the structure summarized below.

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Python (7).

## Repository Contents

- `CHANGES.md` - concise history of maintenance changes
- `Makefile` - local verification entry point
- `README.md` - project overview and local usage notes
- `requirements.txt` - Python dependency or packaging metadata
- `scripts/check-baseline.py` - static legacy GNIP demo checks
- `tests/test_timeframe.py` - local unit coverage for timeframe behavior
- `gnip_search` - source or example code
- `SECURITY.md` - security reporting and disclosure guidance
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: gnip_search
- Dependency and build manifests: requirements.txt
- Entry points or build surfaces: Makefile, step1.py, step2.py
- Test-looking files: scripts/check-baseline.py, tests/test_timeframe.py

## Getting Started

### Prerequisites

- Git
- GNU Make and a POSIX shell
- Python matching the era of the project
- Python 3 for static verification

### Setup

```bash
git clone https://github.com/garethpaul/gnip-light-demo.git
cd gnip-light-demo
python -m pip install -r requirements.txt
```

The setup commands above are derived from repository files. Legacy mobile, Python, or JavaScript samples may require older SDKs or package versions than a modern workstation uses by default.

## Running or Using the Project

- Set `GNIP_USER_NAME`, `GNIP_PASSWORD`, and `GNIP_SEARCH_ENDPOINT` in the local environment before live API calls.
- `GNIP_SEARCH_ENDPOINT` must be an HTTPS URL with a host and no embedded credentials, query string, or fragment.
- `step1.py` prints retrieved data for the sample query.
- `step2.py` writes the sample CSV export; generated exports are intentionally ignored.
- Importing the sample scripts does not trigger live GNIP requests or CSV
  writes; run them directly to execute their sample `main()` functions.
- Missing GNIP environment variables raise a clear configuration error before the request is built.

## Testing and Verification

- Run `make lint`, `make test`, `make build`, and `make check` for static
  syntax, timeframe unit coverage, and credential/dependency/request guardrails
  that do not require GNIP credentials. The `lint`, `test`, and `build` targets
  currently delegate to the static baseline.
- Offline verification uses one explicit, fail-fast Python 3 command while the
  live client remains Python 2.7. The command defaults to `python3`; set
  `PYTHON=/path/to/python3` on the Make invocation to use another compatible
  interpreter for both the checker and its 34 tests.
- `make check` also rejects generated Python bytecode artifacts so local
  compatibility checks do not leave `*.pyc` or `__pycache__` files behind.
- Use the absolute Makefile path to run the same gates from another working
  directory. Make resolves the checker relative to the loaded Makefile rather
  than the caller's directory.
- Dependency-free timeframe behavior tests run on Python 3 in every baseline;
  full legacy syntax checks remain additive when Python 2 is installed.
- GitHub Actions runs the offline baseline on Python 3.10, 3.12, and 3.14
  without credentials or legacy VCS dependency installation.
- Both legacy editable VCS dependencies use HTTPS URLs pinned to immutable 40-character commits. This fixes source selection but does not establish modern runtime compatibility or artifact hash authentication.
- `make check` verifies the sample entry points keep live GNIP requests and
  CSV writes behind `__main__` guards.
- Paged GNIP output filename prefixes are normalized to a conservative filename
  character set before JSON exports are written.
- Query-preview and no-result output mask query text and pagination tokens, and
  printable query errors omit request and provider response payloads and
  messages.
- Geo exports remove only the exact GNIP `.000Z` posted-time suffix so seconds
  ending in zero are not truncated by character-set stripping.
- GNIP request timeout exceptions exit with a clear error instead of falling
  through to result parsing or a traceback.
- GNIP validation and request failures exit with a nonzero status so automation
  cannot mistake rejected input or failed requests for successful runs.
- GNIP date filters must match the documented `YYYY-MM-DD HH:MM` format before
  the API-specific date strings are built.
- GNIP date filters also reject impossible calendar values before the compact
  request payload dates are derived.
- Live GNIP calls still require local credentials and compatible legacy dependencies.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- GNIP credentials must come from `GNIP_USER_NAME`, `GNIP_PASSWORD`, and `GNIP_SEARCH_ENDPOINT`; do not commit credentials or retrieved tweet exports.
- Whitespace-only credential values are rejected, and `GNIP_SEARCH_ENDPOINT`
  must parse as an HTTPS URL with a host and no embedded credentials, query string, or fragment before requests are built.
- GNIP live requests use an explicit timeout. Override it with `GNIP_REQUEST_TIMEOUT` when a slower live API path requires it; the value must be a positive integer number of seconds.
- GNIP request timeout exceptions are handled with a clear error before result
  parsing.
- GNIP date filters reject malformed delimiters before request payload dates are
  derived.
- GNIP date filters reject impossible calendar values before request payload
  dates are derived.
- Paged searches reject blank or repeated continuation tokens and stop at a
  hard 1,000-page ceiling before issuing another authenticated request.
- Link aggregation parses serialized values without code execution and accepts
  only nonblank strings or string collections; malformed fields are counted as
  `InvalidLinks` instead of aborting result processing.
- Link fields are bounded to 64 KiB, 1,000 values, and 4,096 characters per
  value before aggregation.
- Live result processing does not log query payloads or extracted link values.
- GNIP HTTP error responses call `raise_for_status()` so live failures surface instead of being parsed as result data.
- GNIP page bodies are streamed in 64 KiB chunks, capped at 16 MiB after
  decompression, and closed before JSON parsing continues.
- GNIP response pages must decode to objects with list results before records
  are accumulated, paginated, or written to files.
- Activity query payloads include a validated `maxResults` page size capped at
  500; count/timeline payloads omit that activity-only field.

## Security and Privacy Notes

- Review changes touching authentication or token handling; examples from the scan include gnip_search/gnip_search_api.py.
- Review changes touching external API calls or credential-adjacent configuration; examples from the scan include gnip_search/gnip_search_api.py, requirements.txt, step2.py.
- Review changes touching network requests, sockets, or service endpoints; examples from the scan include gnip_search/gnip_search_api.py.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include gnip_search/gnip_search_api.py, step2.py.

## Maintenance Notes

- This is a legacy Python 2 sample. Keep Python 2/API compatibility changes separate from static hardening where practical.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-09-python-bytecode-artifact-guard.md` for the
  bytecode artifact baseline.
- See `docs/plans/2026-06-09-gnip-endpoint-url-parts.md` for the endpoint
  URL-parts guard.
- See `docs/plans/2026-06-09-gnip-sample-entrypoints.md` for the sample
  entrypoint guard.
- See `docs/plans/2026-06-09-make-gate-aliases.md` for local verification
  target guardrails.
- See `docs/plans/2026-06-09-gnip-export-prefix-sanitizer.md` for paged export
  filename prefix sanitization.
- See `docs/plans/2026-06-09-gnip-timeout-exception-handling.md` for GNIP
  request timeout exception handling.
- See `docs/plans/2026-06-09-gnip-date-format-validation.md` for strict GNIP
  date filter validation.
- See `docs/plans/2026-06-09-gnip-date-value-validation.md` for GNIP date
  value validation.
- See `docs/plans/2026-06-10-gnip-pagination-boundary.md` for paged-search cycle
  detection and the hard page limit.
- See `docs/plans/2026-06-12-gnip-link-literal-boundary.md` for safe link-value
  parsing and invalid-field handling.
- See `docs/plans/2026-06-12-gnip-response-body-boundary.md` for streamed GNIP
  page size and network-resource limits.
- See `docs/plans/2026-06-12-vcs-dependency-pinning.md` for immutable legacy
  dependency source selection.
- See `docs/plans/2026-06-14-gnip-max-results-payload.md` for bounded activity
  query page-size construction.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
