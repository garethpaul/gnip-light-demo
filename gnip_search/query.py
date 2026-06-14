try:
    string_types = (basestring,)
    integer_types = (int, long)
except NameError:
    string_types = (str,)
    integer_types = (int,)


DEFAULT_MAX_RESULTS = 100
MAX_RESULTS_PER_PAGE = 500


class QueryPayloadError(ValueError):
    pass


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
    payload = {"query": query}
    if not counts:
        payload["maxResults"] = request_page_size(max_results, paged=paged)
    return payload
