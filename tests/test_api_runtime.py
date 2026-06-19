from __future__ import print_function

import contextlib
import importlib
import io
import sys
import types
import unittest


@contextlib.contextmanager
def redirected_stderr(stream):
    original = sys.stderr
    sys.stderr = stream
    try:
        yield
    finally:
        sys.stderr = original


class APIRuntimeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        twitter_acs = types.ModuleType("acscsv.twitter_acs")
        class FakeTwacsCSV(object):
            def __init__(self, *args, **kwargs):
                pass

        class FakeSimpleNGrams(object):
            def __init__(self, *args, **kwargs):
                pass

        twitter_acs.TwacsCSV = FakeTwacsCSV
        acscsv = types.ModuleType("acscsv")
        acscsv.twitter_acs = twitter_acs
        simple_module = types.ModuleType("simple_n_grams.simple_n_grams")
        simple_module.SimpleNGrams = FakeSimpleNGrams
        simple_package = types.ModuleType("simple_n_grams")
        simple_package.simple_n_grams = simple_module
        requests = types.ModuleType("requests")

        class RequestException(Exception):
            pass

        class Timeout(RequestException):
            pass

        class ConnectionError(RequestException):
            pass

        class HTTPError(RequestException):
            pass

        class Exceptions(object):
            pass

        requests.exceptions = Exceptions()
        requests.exceptions.RequestException = RequestException
        requests.exceptions.Timeout = Timeout
        requests.exceptions.ConnectionError = ConnectionError
        requests.exceptions.HTTPError = HTTPError
        requests.Session = None
        sys.modules["acscsv"] = acscsv
        sys.modules["acscsv.twitter_acs"] = twitter_acs
        sys.modules["simple_n_grams"] = simple_package
        sys.modules["simple_n_grams.simple_n_grams"] = simple_module
        sys.modules["requests"] = requests
        cls.api_module = importlib.import_module("gnip_search.gnip_search_api")

    def test_timeout_diagnostic_is_redacted_and_cleanup_cannot_mask_exit(self):
        requests = self.api_module.requests

        class FakeSession(object):
            def __init__(self):
                self.headers = {}
                self.auth = None

            def post(self, *args, **kwargs):
                raise requests.exceptions.Timeout(
                    "secret-query-and-endpoint-sentinel")

            def close(self):
                raise IOError("cleanup-sentinel")

        original_session = requests.Session
        requests.Session = FakeSession
        try:
            api = object.__new__(self.api_module.GnipSearchAPI)
            api.user = "account"
            api.password = "password-sentinel"
            api.stream_url = "https://example.test/private-endpoint-sentinel"
            api.rule_payload = {"query": "secret-query-sentinel"}
            stderr = io.StringIO()

            with redirected_stderr(stderr):
                with self.assertRaises(SystemExit) as raised:
                    api.req()

            self.assertEqual(1, raised.exception.code)
            diagnostic = stderr.getvalue()
            self.assertIn("GNIP request timed out", diagnostic)
            for secret in (
                "secret-query-and-endpoint-sentinel",
                "cleanup-sentinel",
                "password-sentinel",
                "private-endpoint-sentinel",
                "secret-query-sentinel",
            ):
                self.assertNotIn(secret, diagnostic)
        finally:
            requests.Session = original_session

    def test_query_errors_do_not_retain_provider_payloads(self):
        error = self.api_module.QueryError(
            "GNIP query failed",
            {"query": "secret-query", "next": "secret-token", "bucket": "day"},
            {"results": [{"body": "private tweet"}]},
        )

        self.assertEqual(
            {"query": "<redacted>", "next": "<redacted>", "bucket": "day"},
            error.payload,
        )
        self.assertIsNone(error.response)
        self.assertNotIn("private tweet", repr(error.__dict__))

    def test_wrapper_reuses_its_api_and_propagates_query_failures(self):
        wrapper_module = importlib.import_module("gnip_search.gnip_wrapper")
        api_instances = []
        query_error = self.api_module.QueryError

        class FailingAPI(object):
            def query_api(self, *args, **kwargs):
                raise query_error(
                    "GNIP query failed",
                    {"query": "secret"},
                    {"results": [{"body": "private"}]},
                )

        original_api = wrapper_module.GNIP.api
        wrapper_module.GNIP.api = lambda instance: api_instances.append(FailingAPI()) or api_instances[-1]
        try:
            request = wrapper_module.GNIP("cats", 25)

            with self.assertRaises(self.api_module.QueryError):
                request.get_tweets()

            self.assertEqual(1, len(api_instances))
        finally:
            wrapper_module.GNIP.api = original_api

    def test_query_validation_runs_before_filename_processing(self):
        from gnip_search.query import QueryPayloadError

        api = self.api_module.GnipSearchAPI(
            "account",
            "password",
            "https://example.test/search.json",
        )

        with self.assertRaises(QueryPayloadError):
            api.query_api(None, query=True)


if __name__ == "__main__":
    unittest.main()
