# GNIP Link Literal Boundary

status: completed

## Context

GNIP link aggregation receives a serialized Python literal from the legacy
TwacsCSV adapter. Dynamic execution was removed previously, but parsing still
accepted arbitrary literal shapes and silently converted malformed input into
an empty result. Numeric or mapping literals could fail during iteration or
produce misleading frequency entries.

## Implementation

- Parse serialized values with `ast.literal_eval` in a dependency-free helper.
- Accept only nonblank strings or collections containing nonblank strings.
- Reject expressions, mappings, scalars, empty collections, and mixed values
  with a stable `LinkParseError`.
- Bound serialized fields to 64 KiB, collections to 1,000 values, and each link
  value to 4,096 characters before aggregation.
- Count rejected link fields as `InvalidLinks` without executing input or
  aborting the remaining result stream.
- Remove unconditional query-payload and extracted-link debug output so search
  rules and result URLs do not leak into process logs.
- Run focused parser tests on both Python 2 and Python 3.

## Verification

- `python3 -m unittest discover -s tests -p test_links.py`
- `python2 -m unittest discover -s tests -p test_links.py`
- `make check`
- `git diff --check`
- Mutations restoring direct literal iteration, accepting mappings and code
  expressions, removing resource limits, or logging query/link values must
  fail.
