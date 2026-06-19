#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from gnip_search.query import (
    DEFAULT_MAX_RESULTS,
    MAX_QUERY_BYTES,
    MAX_QUERY_CHARS,
    MAX_RESULTS_PER_PAGE,
    QueryPayloadError,
    build_rule_payload,
    request_page_size,
)


class QueryPayloadTest(unittest.TestCase):
    def test_builds_activity_payload_with_requested_page_size(self):
        self.assertEqual(
            {"query": "cats", "maxResults": 25},
            build_rule_payload("cats", 25),
        )

    def test_uses_default_when_result_count_is_omitted(self):
        self.assertEqual(DEFAULT_MAX_RESULTS, request_page_size(None))

    def test_accepts_integer_strings_from_request_parameters(self):
        self.assertEqual(25, request_page_size("25"))

    def test_caps_single_requests_at_provider_page_limit(self):
        self.assertEqual(MAX_RESULTS_PER_PAGE, request_page_size(10000))

    def test_paged_searches_force_provider_page_limit(self):
        self.assertEqual(MAX_RESULTS_PER_PAGE, request_page_size(25, paged=True))

    def test_count_payload_omits_activity_page_size(self):
        self.assertEqual(
            {"query": "cats"},
            build_rule_payload("cats", 0, counts=True),
        )

    def test_rejects_blank_non_string_control_or_oversized_queries(self):
        invalid_queries = (
            None,
            "",
            "   ",
            123,
            "cats\npassword",
            "x" * (MAX_QUERY_CHARS + 1),
            "😀" * ((MAX_QUERY_BYTES // 4) + 1),
        )
        for query in invalid_queries:
            with self.assertRaises(QueryPayloadError):
                build_rule_payload(query, 25)

    def test_rejects_invalid_page_sizes(self):
        for value in (0, -1, True, 1.5, "", "ten"):
            with self.assertRaises(QueryPayloadError):
                request_page_size(value)


if __name__ == "__main__":
    unittest.main()
