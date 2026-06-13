import unittest

from gnip_search.schema import ResponseShapeError, response_results


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


if __name__ == "__main__":
    unittest.main()
