from __future__ import print_function

import importlib
import os
import shutil
import sys
import tempfile
import types
import unittest


class SampleBehaviorTest(unittest.TestCase):
    def setUp(self):
        self.original_modules = dict(sys.modules)

    def tearDown(self):
        sys.modules.clear()
        sys.modules.update(self.original_modules)

    def test_full_archive_search_fetches_at_most_once(self):
        calls = []

        class FakeGNIP(object):
            def __init__(self, query, query_count):
                calls.append((query, query_count))

            def get_tweets(self):
                return [{"id": "one"}]

        wrapper = types.ModuleType("gnip_search.gnip_wrapper")
        wrapper.GNIP = FakeGNIP
        sys.modules["gnip_search.gnip_wrapper"] = wrapper
        sys.modules.pop("gnip_search.tweets", None)
        tweets_module = importlib.import_module("gnip_search.tweets")

        search = tweets_module.FullArchiveSearch("cats", 25)

        self.assertEqual([], calls)
        self.assertEqual([{"id": "one"}], search.get_data())
        self.assertEqual([{"id": "one"}], search.get_data())
        self.assertEqual([("cats", 25)], calls)

    def test_csv_output_is_not_truncated_when_fetch_fails(self):
        class FailingSearch(object):
            def __init__(self, query, query_count):
                pass

            def get_data(self):
                raise RuntimeError("provider failed")

        tweets_module = types.ModuleType("gnip_search.tweets")
        tweets_module.FullArchiveSearch = FailingSearch
        sys.modules["gnip_search.tweets"] = tweets_module
        sys.modules.pop("step2", None)
        step2 = importlib.import_module("step2")

        temp_dir = tempfile.mkdtemp()
        try:
            output_path = os.path.join(temp_dir, "bliebers.csv")
            with open(output_path, "w") as output_file:
                output_file.write("existing-data\n")

            with self.assertRaises(RuntimeError):
                step2.main(output_path=output_path)

            with open(output_path, "r") as output_file:
                self.assertEqual("existing-data\n", output_file.read())
        finally:
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
