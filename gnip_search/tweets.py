from gnip_wrapper import GNIP


class FullArchiveSearch:
    """
    Class container for tweets
    """

    def __init__(self, query, query_count):
        self.query = query
        self.query_count = query_count
        self.data = self.get_data()

    def get_data(self):
        """
        Returns tweets
        """
        request = GNIP(
            query=self.query,
            query_count=self.query_count)
        return request.get_tweets()
