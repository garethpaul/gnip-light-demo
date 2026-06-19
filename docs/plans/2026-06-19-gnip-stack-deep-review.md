# GNIP Stack Deep Review

status: implementation complete; hosted verification pending

## Scope

Review and reconcile open PRs #5-#13. PR #5 is a separate response-boundary
evidence root. PRs #6-#13 form the maintained Python/Twitter Ads/GNIP stack.

## Findings

1. Response cleanup errors could mask the original stream failure.
2. Raw Requests exception text could disclose account-specific endpoint data.
3. `QueryError` retained request and provider payloads after redacted printing.
4. Queries and continuation tokens lacked complete size/control validation.
5. Response result items and deeply malformed JSON could escape controlled
   schema errors.
6. Posted-time handling accepted invalid calendars and non-UTC values.
7. Python 3 CI did not import the Python-2-only main request module.
8. `FullArchiveSearch` eagerly fetched and callers fetched again, duplicating
   live requests. CSV output could be opened before the second fetch failed.
9. Wrapper query failures were printed and converted to `None`, obscuring a
   nonzero failure path.
10. CodeQL identified the library module's legacy executable demo as a
    clear-text live-result logging path.

## Fix Shape

- Keep validation at query, pagination, response, and timestamp ownership
  boundaries.
- Preserve the primary transport error while closing responses and sessions.
- Use fixed diagnostics and retain only redacted request metadata in errors.
- Make sample retrieval lazy and cached; stage output in the destination
  directory and replace only after a complete render.
- Import and behavior-test the actual request/wrapper path on Python 3 while
  retaining Python 2.7-compatible syntax.

## Provider and Dependency Risk

X currently documents Full-Archive Search and GNIP console access as managed
enterprise products and encourages migration toward X API v2. No live provider
request is made in this review. The historical endpoint, Basic Authentication,
Activity Streams shape, account contract, and two pinned VCS packages remain
deployment-specific risks. Both dependency commits were verified to exist in
their upstream repositories; the Twitter Ads SDK commit is GitHub-verified,
while the older Simple-n-grams commit is not cryptographically verified.
The manifest omits the archived `Gnacs` parser and direct `requests` dependency,
and the Twitter Ads SDK declares floating transitive/build dependencies, so it
is historical provenance rather than a reproducible audited environment.

## Verification

- Red-first fake API and mutation-sensitive unit tests.
- Python syntax/import/runtime matrices and external-directory Make gates.
- Immutable VCS commit existence checks, isolated install/audit where feasible,
  Gitleaks current-tree and history scans, GitHub checks, and CodeQL.
