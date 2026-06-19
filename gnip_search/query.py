try:
    string_types = (basestring,)
    integer_types = (int, long)
except NameError:
    string_types = (str,)
    integer_types = (int,)


DEFAULT_MAX_RESULTS = 100
MAX_RESULTS_PER_PAGE = 500
MAX_QUERY_CHARS = 2048
MAX_QUERY_BYTES = MAX_QUERY_CHARS * 4


class QueryPayloadError(ValueError):
    pass


def validated_query(value):
    if not isinstance(value, string_types) or not value.strip():
        raise QueryPayloadError("query must be a non-empty string")
    if len(value) > MAX_QUERY_CHARS:
        raise QueryPayloadError("query exceeds the %d-character limit" % MAX_QUERY_CHARS)
    try:
        query_bytes = value.encode("utf-8")
    except UnicodeError:
        raise QueryPayloadError("query must be valid UTF-8")
    if len(query_bytes) > MAX_QUERY_BYTES:
        raise QueryPayloadError("query exceeds the %d-byte limit" % MAX_QUERY_BYTES)
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise QueryPayloadError("query contains control characters")
    return value


def request_page_size(value, paged=False):
    if paged:
        return MAX_RESULTS_PER_PAGE
    if value is None:
        value = DEFAULT_MAX_RESULTS
    if isinstance(value, bool) or not isinstance(value, integer_types + string_types):
        raise QueryPayloadError("max_results must be a positive integer")
    try:
        value = int(value)
    except (TypeError, ValueError, OverflowError):
        raise QueryPayloadError("max_results must be a positive integer")
    if value <= 0:
        raise QueryPayloadError("max_results must be a positive integer")
    return min(value, MAX_RESULTS_PER_PAGE)


def build_rule_payload(query, max_results=None, paged=False, counts=False):
    payload = {"query": validated_query(query)}
    if not counts:
        payload["maxResults"] = request_page_size(max_results, paged=paged)
    return payload
