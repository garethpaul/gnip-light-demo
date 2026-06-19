import unittest

from gnip_search.schema import (
    ResponseShapeError,
    decode_response_payload,
    response_results,
)


class ResponseShapeTest(unittest.TestCase):
    def test_accepts_results_list(self):
        results = [{"id": "one"}]

        self.assertEqual(results, response_results({"results": results}))

    def test_defaults_missing_results_to_empty_list(self):
        self.assertEqual([], response_results({}))

    def test_rejects_non_object_pages(self):
        for payload in (None, [], "value", 1, True):
            with self.assertRaises(ResponseShapeError):
                response_results(payload)

    def test_rejects_non_list_results(self):
        for results in (None, {}, "value", 1, True):
            with self.assertRaises(ResponseShapeError):
                response_results({"results": results})

    def test_rejects_non_object_result_items(self):
        for result in (None, [], "value", 1, True):
            with self.assertRaises(ResponseShapeError):
                response_results({"results": [{"id": "valid"}, result]})

    def test_deep_or_malformed_json_fails_with_a_controlled_shape_error(self):
        for payload in (b"not-json", (b"[" * 2000) + (b"]" * 2000)):
            with self.assertRaises(ResponseShapeError):
                decode_response_payload(payload)


if __name__ == "__main__":
    unittest.main()
