# GNIP Pagination Boundary

status: completed

## Context

Paged GNIP searches follow every provider-supplied `next` token with no cycle
detection or page ceiling. A repeated token or unexpectedly long chain can keep
issuing authenticated requests while growing in-memory results and export
output without bound.

## Priority

Pagination metadata is an external response boundary. Bounding it prevents a
malformed or hostile response from turning an export into an infinite request
loop or unbounded resource consumer.

## Implementation

- Add a Python 2/3-compatible pagination guard with a 1,000-page ceiling.
- Require next tokens to be non-empty strings.
- Reject repeated next tokens before another request is issued.
- Raise the existing query error type with actionable pagination details.
- Add executable tests for valid tokens, blank/non-string tokens, repetition,
  and the hard page limit.
- Extend the static baseline and operational documentation.

## Verification

- `python3 -m unittest discover -s tests`
- `make check`
- `make lint`
- `make test`
- `make build`
- `git diff --check`
- Mutations disabling cycle detection or the page ceiling must fail.
- Hosted Python 3.10/3.12/3.14 characterization workflow.
