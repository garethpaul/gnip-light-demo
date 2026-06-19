import unittest

from gnip_search.pagination import MAX_TOKEN_BYTES, PaginationError, PaginationGuard


class PaginationGuardTest(unittest.TestCase):
    def test_accepts_unique_tokens_within_page_limit(self):
        guard = PaginationGuard(max_pages=3)

        self.assertEqual("page-2", guard.accept("page-2"))
        self.assertEqual("page-3", guard.accept("page-3"))
        self.assertEqual(3, guard.page_count)

    def test_rejects_blank_and_non_string_tokens(self):
        for token in (None, "", "   ", 123):
            with self.assertRaises(PaginationError):
                PaginationGuard().accept(token)

    def test_rejects_oversized_or_control_bearing_tokens(self):
        for token in ("x" * (MAX_TOKEN_BYTES + 1), "page\n2", "page\x002"):
            with self.assertRaises(PaginationError):
                PaginationGuard().accept(token)

    def test_rejects_repeated_tokens(self):
        guard = PaginationGuard()
        guard.accept("same-token")

        with self.assertRaises(PaginationError):
            guard.accept("same-token")

    def test_rejects_tokens_beyond_page_limit(self):
        guard = PaginationGuard(max_pages=2)
        guard.accept("page-2")

        with self.assertRaises(PaginationError):
            guard.accept("page-3")

    def test_rejects_invalid_page_limits(self):
        for max_pages in (0, -1, True, "10"):
            with self.assertRaises(ValueError):
                PaginationGuard(max_pages=max_pages)


if __name__ == "__main__":
    unittest.main()
