# GNIP Endpoint URL Parts

status: completed

## Context

`GNIP_SEARCH_ENDPOINT` is local configuration, but it feeds directly into live
request construction. The existing guard requires HTTPS and a host; it should
also reject credentials, query strings, and fragments so the endpoint remains a
plain service URL and secrets stay in the requests auth fields.

## Completed Scope

- Rejected embedded usernames and passwords in `GNIP_SEARCH_ENDPOINT`.
- Rejected query strings and fragments in `GNIP_SEARCH_ENDPOINT`.
- Extended the static baseline, README, VISION, and CHANGES notes.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
