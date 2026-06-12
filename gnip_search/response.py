MAX_RESPONSE_BYTES = 16 * 1024 * 1024
RESPONSE_CHUNK_BYTES = 64 * 1024


class ResponseBodyError(ValueError):
    pass


def read_response_body(response):
    chunks = []
    total_bytes = 0
    try:
        for chunk in response.iter_content(chunk_size=RESPONSE_CHUNK_BYTES):
            if not chunk:
                continue
            total_bytes += len(chunk)
            if total_bytes > MAX_RESPONSE_BYTES:
                raise ResponseBodyError(
                    "GNIP response exceeds the %d-byte limit" % MAX_RESPONSE_BYTES)
            chunks.append(chunk)
    finally:
        response.close()
    return b"".join(chunks)
