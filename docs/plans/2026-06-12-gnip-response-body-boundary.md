# GNIP Response Body Boundary

status: completed

## Context

GNIP requests have a validated timeout, and paged searches reject malformed or
repeated continuation tokens and stop after 1,000 pages. Each individual page
is still loaded through `requests.Response.text`, which buffers the complete
provider response without an application-level byte limit.

A fast oversized or decompression-expanded response can therefore consume far
more process memory than one search page requires before JSON parsing starts.

## Priority

The page-count ceiling bounds request amplification but not per-page memory.
Adding a streamed response boundary makes the live network path fail
predictably under oversized provider output.

## Prioritized Backlog

1. Stream GNIP response bodies instead of accessing `Response.text`.
2. Limit each decompressed page to 16 MiB using 64 KiB chunks.
3. Close responses after successful, oversized, or failed reads and close the
   per-request session on every exit path.
4. Preserve timeout, HTTP status, pagination, and JSON error behavior.
5. Add dependency-free Python 2/3 tests and static mutation contracts.

## Implementation

- Add `gnip_search.response.read_response_body` with explicit byte and chunk
  constants plus a dedicated `ResponseBodyError`.
- Count yielded `iter_content` bytes, ignore empty keep-alive chunks, and reject
  the first chunk that crosses the limit.
- Pass `stream=True` to `Session.post`, call `raise_for_status`, and hand the
  response to the bounded reader.
- Close the request session in `finally` after response processing or network
  failure handling.
- Extend tests, baseline checks, README, SECURITY, VISION, and CHANGES.

## Verification

- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
- `python3 scripts/check-baseline.py`
- `make check`
- `make lint`
- `make test`
- `make build`
- Python 2 syntax compilation and tests when available
- `git diff --check`
- Mutations removing `stream=True`, the byte counter, oversized rejection,
  response closure, session closure, or bounded-reader routing must fail.

No live GNIP requests or credentials are required for this change.

## Work Completed

- Added a streamed 16 MiB decompressed response limit using 64 KiB chunks,
  ignored empty keep-alive chunks, and rejected the first chunk crossing the
  boundary.
- Preserved timeout, HTTP status, pagination, and JSON error handling while
  guaranteeing response and per-request session cleanup on every exit path.
- Added dependency-free Python 2/3 tests and static contracts for streamed
  routing, byte accounting, oversize rejection, and cleanup.

## Verification Completed

- All four Make gates and `git diff --check` passed locally under Python 3.12
  and Python 2.7; all 17 tests passed in both interpreter paths.
- Implementation push run `27393392384` and pull-request run `27393397945`
  passed at commit `c817b080580cbcb3df4d5bcf27e8caa55ae48cce` across Python
  3.10, 3.12, and 3.14.
- Post-merge push run `27393412678` and CodeQL run `27402321656` passed at
  default-branch merge commit `27c94967ea278f0c1276edbda6238acfad241b88`.
- Mutations removing `stream=True`, byte accounting, oversized rejection,
  response closure, session closure, or bounded-reader routing were rejected.
