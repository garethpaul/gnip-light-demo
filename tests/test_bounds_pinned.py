"""The reviewed numeric bounds must be pinned independently of the constants.

Every other test derives its fixture from the constant it is checking, e.g.
`"x" * (MAX_QUERY_CHARS + 1)`. That proves the limit is *enforced* but never that
it is the *reviewed value*: raise the constant and the fixture grows with it, so
the test still passes. `scripts/check-baseline.py` was the only other pin, and it
used substring matching (`"MAX_QUERY_CHARS = 2048" in query_source`), which digit
extension satisfies — `MAX_QUERY_CHARS = 20480` contains `MAX_QUERY_CHARS = 2048`.
Together that let all six bounds be widened tenfold with `make check` green.

Hardcoding the expected values here is the pattern oscars-sample-stream already
uses (`"x" * 513`, `range(101)` written out rather than derived) and that
Excel-Parser uses for its workbook cap: the expected number lives somewhere that
does not move when the constant does, so the two cannot drift together.

Changing a bound deliberately should mean changing it here too -- that is the
review prompt this file exists to create.
"""
import unittest

from gnip_search.links import (
    MAX_LINK_CHARS,
    MAX_LINK_VALUES,
    MAX_SERIALIZED_LINK_CHARS,
)
from gnip_search.pagination import DEFAULT_MAX_PAGES, MAX_TOKEN_BYTES
from gnip_search.query import MAX_QUERY_CHARS


class PinnedBoundsTests(unittest.TestCase):
    def test_query_bounds_match_the_reviewed_values(self):
        self.assertEqual(2048, MAX_QUERY_CHARS)

    def test_link_bounds_match_the_reviewed_values(self):
        self.assertEqual(65536, MAX_SERIALIZED_LINK_CHARS)
        self.assertEqual(1000, MAX_LINK_VALUES)
        self.assertEqual(4096, MAX_LINK_CHARS)

    def test_pagination_bounds_match_the_reviewed_values(self):
        self.assertEqual(1000, DEFAULT_MAX_PAGES)
        self.assertEqual(4096, MAX_TOKEN_BYTES)


if __name__ == "__main__":
    unittest.main()
