# AGENTS.md

## Repository purpose

`garethpaul/gnip-light-demo` is a Python project. The checked-in files describe a Python project with the structure summarized below.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `tests` - tests and fixtures
- `requirements.txt` - Python runtime dependencies
- `gnip_search` - repository source or sample assets

## Development commands

- Install dependencies: `python3 -m pip install -r requirements.txt`
- Full baseline: `make check`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: Python (7).
- Prefer dependency-free tests or stdlib checks when legacy packages are unavailable.

## Testing guidance

- Test-related files detected: `tests/`, `tests/test_timeframe.py`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- GNIP credentials must come from `GNIP_USER_NAME`, `GNIP_PASSWORD`, and `GNIP_SEARCH_ENDPOINT`; do not commit credentials or retrieved tweet exports.
- Whitespace-only credential values are rejected, and `GNIP_SEARCH_ENDPOINT` must parse as an HTTPS URL with a host and no embedded credentials, query string, or fragment before requests are built.
- GNIP live requests use an explicit timeout. Override it with `GNIP_REQUEST_TIMEOUT` when a slower live API path requires it; the value must be a positive integer number of seconds.
- GNIP request timeout exceptions are handled with a clear error before result parsing.
- GNIP validation and request failures exit with a nonzero status; preserve the
  successful exit used only by the redacted query-preview mode.
- Validate GNIP response objects and list results before downstream processing.
- Build activity query payloads through `gnip_search.query.build_rule_payload`;
  preserve positive page-size validation, the 500-result ceiling, and omission
  of `maxResults` from count/timeline payloads.
- GNIP date filters reject malformed delimiters before request payload dates are derived.
- GNIP link aggregation must use `gnip_search.links.parse_link_values`; never
  restore `exec`, `eval`, or unvalidated iteration over parsed literal shapes.
- Preserve the link parser's serialized-size, collection-count, and per-value
  limits when changing provider parsing.
- Do not log query payloads, extracted link values, credentials, or retrieved
  tweet content.
- Remove only the exact GNIP `.000Z` posted-time suffix in geo exports; do not
  restore character-set `strip` handling.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.

Offline verification uses one explicit, fail-fast Python 3 command while the
live client remains Python 2.7. Override `PYTHON` only with a compatible Python
3 command so the checker and its unit discovery use the same interpreter.
