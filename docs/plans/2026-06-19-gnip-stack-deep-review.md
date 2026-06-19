# GNIP Stack Deep Review

status: completed

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

## Verification Completed

- 49 tests passed on Python 3.10.16, 3.11.11, 3.12.1, and 3.14.5.
- All Make aliases, the external-directory gate, and `git diff --check` passed.
- 25 runtime and test files parsed with Python 2-compatible grammar. A Python
  2.7 runtime was unavailable locally; uv has no macOS ARM build and Docker was
  unresponsive.
- Seven hostile mutations were rejected across query, pagination, response,
  timestamp, wrapper, sample-caching, and diagnostic boundaries.
- Both immutable VCS commits were verified upstream. A direct no-dependency
  package audit reported no known vulnerabilities while warning that the
  manifest is not fully hashed or transitively pinned.
- Gitleaks current-tree and full-history scans found no exposures. GitHub
  CodeQL and Dependabot reported zero open alerts before the aggregate review.
- Hosted push Check run `27849168447` and pull-request Check run `27849170049`
  passed on Python 3.10, 3.12, and 3.14 at
  `bd583c637681d143c1681311e2cd9bf78d877caa`.
- Hosted CodeQL run `27849168641` passed for Actions and Python, and aggregate
  CodeQL check `82424708835` passed after removal of the legacy live-result
  logging block.
- No live GNIP/X credentials, endpoints, provider payloads, or requests were
  used.
