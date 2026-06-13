import unittest

from gnip_search.privacy import REDACTED_VALUE, redacted_rule_payload


class DiagnosticPrivacyTest(unittest.TestCase):
    def test_redacts_query_and_pagination_token_without_mutating_input(self):
        payload = {
            "query": "private search terms",
            "next": "private-page-token",
            "fromDate": "202606010000",
            "bucket": "day",
        }

        preview = redacted_rule_payload(payload)

        self.assertEqual(REDACTED_VALUE, preview["query"])
        self.assertEqual(REDACTED_VALUE, preview["next"])
        self.assertEqual("202606010000", preview["fromDate"])
        self.assertEqual("day", preview["bucket"])
        self.assertEqual("private search terms", payload["query"])
        self.assertEqual("private-page-token", payload["next"])

    def test_accepts_payload_without_sensitive_fields(self):
        self.assertEqual(
            {"fromDate": "202606010000"},
            redacted_rule_payload({"fromDate": "202606010000"}),
        )


if __name__ == "__main__":
    unittest.main()
