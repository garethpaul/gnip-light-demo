## GNIP Light Demo Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

GNIP Light Demo is a Python sample for GNIP/Twitter full-archive search and
related API exploration.

The repository is useful as a small historical demo around GNIP search wrappers,
tweet retrieval, and Twitter ads SDK dependencies. Setup notes live in
[`README.md`](README.md).

The goal is to keep the demo credential-safe and understandable while making
legacy dependency and API assumptions explicit.

The current focus is:

Priority:

- Preserve the simple full-archive search example
- Keep GNIP/Twitter credentials out of source control
- Make Python 2 and editable dependency assumptions visible
- Avoid committing retrieved tweet exports or private customer data
- Keep `make lint`, `make test`, `make build`, and `make check` passing for
  parser, credential, and dependency transport guardrails

Current baseline:

- `make lint`, `make test`, `make build`, and `make check` verify legacy
  Python syntax when Python 2 is available.
- Timeframe parsing and invalid-range fallback have local unit coverage.
- Geo exports validate ISO-8601 UTC posted times and reject invalid calendars
  or non-UTC offsets before normalization.
- Dependency-free timeframe tests run on Python 3.10, 3.12, and 3.14 in hosted
  CI while full Python 2 checks remain optional and additive.
- API-supplied link data is parsed with `ast.literal_eval`, not `exec`.
- Editable dependencies use HTTPS rather than unauthenticated `git://` transport.
- GNIP credentials are read from environment variables, and
  `GNIP_SEARCH_ENDPOINT` must parse as an HTTPS URL with a host and no embedded credentials, query string, or fragment.
- Missing GNIP credentials, invalid request-timeout configuration, slow GNIP requests, and HTTP error responses fail before result parsing.
- GNIP page responses are streamed through a 16 MiB decompressed-size ceiling
  and release response/session resources on all exit paths.
- Require GNIP response objects and list results before downstream processing.
- Activity queries send a validated `maxResults` value capped at the provider's
  500-result page boundary, while count queries omit that field.
- Queries remain within the provider's documented 2,048-character limit, and
  continuation tokens remain bounded and control-free.
- Provider JSON and result-item shapes fail closed before downstream handling.
- Fixed transport diagnostics and redacted exceptions keep credentials,
  endpoints, queries, tokens, and provider payloads out of errors.
- Sample retrieval is single-fetch and CSV replacement is atomic.
- Local environment files and sample exports stay ignored.
- Baseline checks should not leave generated Python bytecode artifacts in the
  working tree.
- Sample entry points keep live GNIP calls and CSV writes behind main guards so
  imports are safe during inspection or future tests.
- Paged GNIP output filename prefixes are normalized to a conservative filename
  character set before JSON exports are written.
- Paged GNIP searches reject malformed or repeated continuation tokens and
  stop at a 1,000-page ceiling.
- GNIP link aggregation accepts only nonblank string literals and collections,
  and records malformed serialized fields without executing them.
- Serialized link fields, collection cardinality, and individual values remain
  bounded before parsing and aggregation.
- Query payloads and extracted link values are not logged during result
  processing.
- Query-preview and exception diagnostics keep query, pagination-token, request,
  and provider response content and messages out of printable output.
- GNIP request timeout exceptions fail with a clear error before result parsing.
- GNIP validation and request failures exit with a nonzero status while the
  redacted query-preview mode remains a successful no-request operation.
- GNIP date filters must match `YYYY-MM-DD HH:MM` before API request dates are
  derived.
- GNIP date filters reject impossible calendar values before compact API request
  dates are derived.
- Local verification targets stay available while the legacy Python 2 runtime
  remains static-check only.
- Offline verification uses one explicit, fail-fast Python 3 command. The
  historical client retains Python 2.7-compatible syntax, but no supported or
  reproducible Python 2 live environment is claimed.
- The primary API and wrapper path imports and runs under Python 3, while live
  legacy VCS dependencies and managed GNIP/X enterprise access remain explicit
  deployment risks.
- The current manifest is historical provenance rather than a lockfile: it
  omits direct `Gnacs` and `requests` pins and leaves SDK transitive/build
  dependencies floating.

Next priorities:

- Add credential setup and sample query documentation
- Port to supported Python and maintained Twitter/X API clients if revived
- Add tests around timeframe handling and total-result pagination semantics
- Keep GNIP date filters strict if query construction is modernized
- Keep impossible calendar values out of live GNIP date payloads
- Keep per-page response memory bounded alongside pagination count limits
- Separate publishable fixtures from live API data

Contribution rules:

- One PR = one focused API, wrapper, dependency, or documentation change.
- Do not commit tokens, account credentials, or retrieved private data.
- Verify live calls only with local credentials.
- Document dependency and API version changes.
- Pin legacy VCS dependencies to reviewed full commit SHAs.

## Security And Data

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

GNIP/Twitter APIs may expose private credentials and sensitive social data.
Credentials must stay in local environment/config, and retrieved data should not
be committed unless it is explicitly public and safe as a fixture.

## What We Will Not Merge (For Now)

- API credentials, tokens, or customer exports
- Bulk social data dumps
- Live-only tests as the default check path
- Dependency changes that obscure API compatibility

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
