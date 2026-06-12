try:
    string_types = (basestring,)
except NameError:
    string_types = (str,)


DEFAULT_MAX_PAGES = 1000


class PaginationError(ValueError):
    pass


class PaginationGuard(object):
    def __init__(self, max_pages=DEFAULT_MAX_PAGES):
        if not isinstance(max_pages, int) or isinstance(max_pages, bool) or max_pages <= 0:
            raise ValueError("max_pages must be a positive integer")

        self.max_pages = max_pages
        self.page_count = 1
        self.seen_tokens = set()

    def accept(self, token):
        if not isinstance(token, string_types) or not token.strip():
            raise PaginationError("GNIP pagination token must be a non-empty string")
        if token in self.seen_tokens:
            raise PaginationError("GNIP pagination token repeated")
        if self.page_count >= self.max_pages:
            raise PaginationError("GNIP pagination exceeded the %d-page limit" % self.max_pages)

        self.seen_tokens.add(token)
        self.page_count += 1
        return token
