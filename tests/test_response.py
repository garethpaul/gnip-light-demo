import unittest

from gnip_search.response import (
    MAX_RESPONSE_BYTES,
    RESPONSE_CHUNK_BYTES,
    ResponseBodyError,
    read_response_body,
)


class FakeResponse(object):
    def __init__(self, chunks=None, error=None, close_error=None):
        self.chunks = chunks or []
        self.error = error
        self.close_error = close_error
        self.closed = False
        self.chunk_sizes = []

    def iter_content(self, chunk_size):
        self.chunk_sizes.append(chunk_size)
        for chunk in self.chunks:
            yield chunk
        if self.error:
            raise self.error

    def close(self):
        self.closed = True
        if self.close_error:
            raise self.close_error


class ResponseBodyTest(unittest.TestCase):
    def test_accepts_exact_limit_and_ignores_empty_chunks(self):
        response = FakeResponse([b"", b"a" * MAX_RESPONSE_BYTES])

        payload = read_response_body(response)

        self.assertEqual(MAX_RESPONSE_BYTES, len(payload))
        self.assertEqual([RESPONSE_CHUNK_BYTES], response.chunk_sizes)
        self.assertTrue(response.closed)

    def test_rejects_payload_over_limit_and_closes_response(self):
        response = FakeResponse([
            b"a" * MAX_RESPONSE_BYTES,
            b"b",
        ])

        with self.assertRaises(ResponseBodyError):
            read_response_body(response)

        self.assertTrue(response.closed)

    def test_closes_response_when_stream_iteration_fails(self):
        response = FakeResponse([b"partial"], IOError("stream failed"))

        with self.assertRaises(IOError):
            read_response_body(response)

        self.assertTrue(response.closed)

    def test_close_failure_does_not_mask_stream_failure(self):
        response = FakeResponse(
            [b"partial"],
            IOError("stream failed"),
            IOError("close failed"),
        )

        with self.assertRaises(IOError) as raised:
            read_response_body(response)

        self.assertIn("stream failed", str(raised.exception))

        self.assertTrue(response.closed)

    def test_rejects_non_byte_response_chunks(self):
        response = FakeResponse(["provider-text"])

        with self.assertRaises(ResponseBodyError):
            read_response_body(response)

        self.assertTrue(response.closed)


if __name__ == "__main__":
    unittest.main()
