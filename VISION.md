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
- Keep the static safety baseline passing for parser, credential, and dependency transport guardrails

Current baseline:

- `make check` verifies legacy Python syntax when Python 2 is available.
- Timeframe parsing and invalid-range fallback have local unit coverage.
- API-supplied link data is parsed with `ast.literal_eval`, not `exec`.
- Editable dependencies use HTTPS rather than unauthenticated `git://` transport.
- GNIP credentials are read from environment variables.
- Missing GNIP credentials and HTTP error responses fail before result parsing.
- Local environment files and sample exports stay ignored.

Next priorities:

- Add credential setup and sample query documentation
- Port to supported Python and maintained Twitter/X API clients if revived
- Add tests around query construction and timeframe handling
- Separate publishable fixtures from live API data

Contribution rules:

- One PR = one focused API, wrapper, dependency, or documentation change.
- Do not commit tokens, account credentials, or retrieved private data.
- Verify live calls only with local credentials.
- Document dependency and API version changes.

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
