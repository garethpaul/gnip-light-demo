import unittest

from gnip_search.links import (
    LinkParseError,
    MAX_LINK_CHARS,
    MAX_LINK_VALUES,
    MAX_SERIALIZED_LINK_CHARS,
    parse_link_values,
)


class LinkValueParserTest(unittest.TestCase):
    def test_accepts_string_and_collection_literals(self):
        self.assertEqual(["https://example.com/a"],
                         parse_link_values("'https://example.com/a'"))
        self.assertEqual(["https://example.com/a", "https://example.com/b"],
                         parse_link_values(
                             "['https://example.com/a', 'https://example.com/b']"))
        self.assertEqual(["https://example.com/a", "https://example.com/b"],
                         parse_link_values(
                             "('https://example.com/a', 'https://example.com/b')"))

    def test_rejects_code_expressions(self):
        with self.assertRaises(LinkParseError):
            parse_link_values("__import__('os').system('echo unsafe')")

    def test_rejects_malformed_or_blank_input(self):
        for value in (None, "", "   ", "[", 123):
            with self.assertRaises(LinkParseError):
                parse_link_values(value)

    def test_rejects_scalar_and_mapping_literals(self):
        for value in ("123", "None", "{'url': 'https://example.com'}"):
            with self.assertRaises(LinkParseError):
                parse_link_values(value)

    def test_rejects_empty_or_mixed_collections(self):
        for value in ("[]", "['']", "['https://example.com', 123]"):
            with self.assertRaises(LinkParseError):
                parse_link_values(value)

    def test_rejects_oversized_serialized_input(self):
        value = "'a'" + (" " * MAX_SERIALIZED_LINK_CHARS)
        with self.assertRaises(LinkParseError):
            parse_link_values(value)

    def test_rejects_too_many_or_oversized_link_values(self):
        too_many = repr(["a"] * (MAX_LINK_VALUES + 1))
        oversized = repr("a" * (MAX_LINK_CHARS + 1))

        for value in (too_many, oversized):
            with self.assertRaises(LinkParseError):
                parse_link_values(value)


if __name__ == "__main__":
    unittest.main()
