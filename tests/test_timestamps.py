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
            "2026-06-13T11:44:10",
            remove_millisecond_utc_suffix("2026-06-13T11:44:10Z"),
        )

    def test_accepts_fractional_utc_seconds_and_normalizes_to_whole_seconds(self):
        self.assertEqual(
            "2026-06-13T11:44:10",
            remove_millisecond_utc_suffix("2026-06-13T11:44:10.123456Z"),
        )

    def test_rejects_invalid_calendar_values_and_non_utc_offsets(self):
        for value in (
            "2026-02-30T11:44:10.000Z",
            "2026-06-13 11:44:10.000Z",
            "2026-06-13T11:44:10+01:00",
            "2026-06-13T11:44:10",
        ):
            with self.assertRaises(ValueError):
                remove_millisecond_utc_suffix(value)

    def test_rejects_non_string_or_empty_values(self):
        for value in (None, "", ".000Z", 0, [], {}):
            with self.assertRaises(ValueError):
                remove_millisecond_utc_suffix(value)


if __name__ == "__main__":
    unittest.main()
