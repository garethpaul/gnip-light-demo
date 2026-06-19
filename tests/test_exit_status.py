import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_PATH = os.path.join(ROOT, "gnip_search", "gnip_search_api.py")


class ExitStatusContractTest(unittest.TestCase):
    def test_failures_exit_nonzero_and_query_preview_remains_successful(self):
        with open(API_PATH, "r") as source_file:
            source = source_file.read()

        failure_markers = (
            "Invalid %s-date format",
            "Invalid %s-date value",
            "Invalid count bucket",
            "except requests.exceptions.Timeout:",
            "except requests.exceptions.ConnectionError:",
            "GNIP returned an HTTP error",
            "except requests.exceptions.RequestException:",
            "except (ResponseBodyError, IOError):",
        )
        for marker in failure_markers:
            marker_start = source.index(marker)
            failure_block = source[marker_start:marker_start + 300]
            self.assertIn("sys.exit(1)", failure_block, marker)

        preview_start = source.index("        if query:")
        preview_end = source.index("\n\n        self.doc", preview_start)
        preview_block = source[preview_start:preview_end]
        self.assertIn("sys.exit()", preview_block)
        self.assertNotIn("sys.exit(1)", preview_block)
        self.assertEqual(8, source.count("sys.exit(1)"))
        self.assertEqual(1, source.count("sys.exit()"))
        self.assertIn(
            'json.dumps(redacted_rule_payload(self.rule_payload), sort_keys=True)',
            source,
        )


if __name__ == "__main__":
    unittest.main()
