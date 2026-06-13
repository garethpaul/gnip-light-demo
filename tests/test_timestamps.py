import unittest

from gnip_search.timestamps import remove_millisecond_utc_suffix


class PostedTimeSuffixTest(unittest.TestCase):
    def test_preserves_seconds_ending_in_zero(self):
        self.assertEqual(
            "2026-06-13T11:44:10",
            remove_millisecond_utc_suffix("2026-06-13T11:44:10.000Z"),
        )
        self.assertEqual(
            "2026-06-13T11:44:00",
            remove_millisecond_utc_suffix("2026-06-13T11:44:00.000Z"),
        )

    def test_removes_suffix_from_ordinary_seconds(self):
        self.assertEqual(
            "2026-06-13T11:44:37",
            remove_millisecond_utc_suffix("2026-06-13T11:44:37.000Z"),
        )

    def test_leaves_values_without_exact_suffix_unchanged(self):
        self.assertEqual(
            "2026-06-13T11:44:10Z",
            remove_millisecond_utc_suffix("2026-06-13T11:44:10Z"),
        )

    def test_rejects_non_string_or_empty_values(self):
        for value in (None, "", ".000Z", 0, [], {}):
            with self.assertRaises(ValueError):
                remove_millisecond_utc_suffix(value)


if __name__ == "__main__":
    unittest.main()
