## GNIP Light Demo Vision

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
