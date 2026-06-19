try:
    from .gnip_wrapper import GNIP
except (ImportError, ValueError):
    from gnip_wrapper import GNIP


_NOT_LOADED = object()


class FullArchiveSearch:
    """
    Class container for tweets
    """

    def __init__(self, query, query_count):
        self.query = query
        self.query_count = query_count
        self.data = _NOT_LOADED

    def get_data(self):
        """
        Returns tweets
        """
        if self.data is _NOT_LOADED:
            request = GNIP(
                query=self.query,
                query_count=self.query_count)
            self.data = request.get_tweets()
        return self.data
