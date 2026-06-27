# Changes

## 2026-06-26 17:46 PDT - P2 - Support spaced Makefile paths

### Summary

Completed the pending location-independent Make fix so absolute Makefiles
loaded from spaced checkout paths still resolve the repository root and run the
full offline gate.

### Work completed

- Encoded spaces before selecting the final entry in `MAKEFILE_LIST`, then
  restored them only after deriving the absolute repository root.
- Added a full-gate regression that invokes the absolute Makefile from an
  external directory under a spaced checkout path.
- Preserved hostile `ROOT` override protection and the shared Python preflight.

### Threads

- Continued: `fix/make-space-safe-root-20260627` — audited and completed the
  existing unmerged branch; no additional thread was started.

### Files changed

- `Makefile` — derive `ROOT` without splitting a spaced Makefile path.
- `tests/test_baseline_contract.py` — exercise the complete external spaced-path
  invocation.
- `scripts/check-baseline.py` — enforce the new root expression and regression.
- `AGENTS.md`, `README.md`, and
  `docs/plans/2026-06-13-location-independent-make.md` — synchronize the
  maintained verification contract and evidence.

### Validation

- `make check`, `make lint`, `make test`, and `make build` — passed all 56
  tests and baseline checks.
- `/usr/bin/make -C /tmp -f "$PWD/Makefile" check` — passed from an external
  caller directory.
- `/usr/bin/make ROOT=/tmp/hostile check` — passed with the caller override
  ignored.
- Hosted matrix evidence recorded by the branch — the full gate passed under
  GNU Make 4.2 and 4.4 from a spaced checkout.
- `git diff --check` — passed.
- An extra direct `py_compile` audit created forbidden `__pycache__` artifacts;
  the baseline contract rejected them as designed. The generated files were
  removed and the authoritative `make check` gate passed again.

### Bugs / findings

- P2 developer workflow: GNU Make tokenized a spaced absolute Makefile path in
  `MAKEFILE_LIST`, redirecting recipe paths away from the repository.

### Blockers

- Python 2 is unavailable locally; the optional syntax-only probe was skipped.

### Next action

- Open a focused pull request, run the required review, and merge only the exact
  head after hosted checks pass.

## 2026-06-26T22:54:06Z

- **Priority:** Security and exported-data integrity.
- **Summary:** Replaced character-set stripping of provider actor IDs with an
  exact `id:twitter.com:<digits>` boundary so malformed or formula-like values
  cannot be written into the sample CSV.
- **Files:** `step2.py`, `tests/test_samples.py`,
  `scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`, and
  `CHANGES.md`.
- **Tests:** Added atomic rejection and canonical numeric output regressions;
  `make check` passes all 55 Python 3 tests and baseline contracts.
- **Findings:** Existing atomic publication already preserves prior output when
  rendering raises, so validation belongs inside the staged render loop.
- **Blockers:** Python 2 is unavailable locally; the repository's supported
  Python 3 gate and optional syntax-only Python 2 probe remain authoritative.
- **Next action:** Open a focused pull request and require hosted checks on its
  exact head SHA.

## 2026-06-19

- Offline verification uses one explicit, fail-fast Python 3 command. No
  supported or reproducible Python 2 live environment is claimed.
- Kept optional Python 2 verification syntax-only so unsupported interpreters
  cannot run the Python 3 characterization suite, and report the exact
  interpreter used for that syntax probe.
- Deep-reviewed PRs #5-#13 and reconciled the separate hosted-evidence root
  with the maintained linear stack.
- Made the primary request and wrapper modules importable on Python 3 while
  preserving Python 2.7-compatible syntax.
- Documented that the two VCS pins do not form a complete lockfile: direct
  `Gnacs`/`requests` dependencies are absent and SDK transitive/build
  dependencies remain floating.
- Added fixed redacted transport diagnostics, cleanup-error precedence,
  non-byte response rejection, controlled malformed/deep-JSON failures, and
  object-only result validation.
- Removed the library module's legacy executable demo that printed live query
  results; explicit sample entry points remain in `step1.py` and `step2.py`.
- Bounded provider queries to 2,048 characters and continuation tokens to 4
  KiB, rejecting blank/control-bearing values before filename or network use.
- Validated and normalized GNIP UTC posted times instead of accepting malformed
  calendars or non-UTC offsets.
- Removed duplicate sample API fetches and made CSV replacement atomic so
  failed retrieval or rendering cannot truncate existing output.

## 2026-06-16

- GNIP validation and request failures now exit with a nonzero status while the
  redacted query-preview mode retains its successful exit.
- Offline verification uses one explicit, fail-fast Python 3 command while the
  live client remains Python 2.7. The Make gates now support a compatible
  `PYTHON` override and reject missing or non-Python-3 commands before running
  the checker.

- Restored activity-query `maxResults` payload construction with positive
  integer validation, a 500-result per-request ceiling, and count-query
  separation.

## 2026-06-13

- Made GNIP verification independent of the caller's working directory by
  resolving the baseline checker from the loaded Makefile.
- Validated GNIP response objects and list results before accumulation,
  pagination, and optional file output.
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
