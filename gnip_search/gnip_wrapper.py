from gnip_search_api import GnipSearchAPI
from gnip_search_api import QueryError as GNIPQueryError
from timeframe import Timeframe
import datetime
import os
import urlparse


class GNIPConfigurationError(Exception):
    pass


def required_environment(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise GNIPConfigurationError("Missing required environment variable: %s" % name)
    return value


def required_https_endpoint(name):
    value = required_environment(name)
    parsed = urlparse.urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc:
        raise GNIPConfigurationError("%s must be an HTTPS URL with a host" % name)
    return value


class GNIP:
    """
    Container wrapper for the GNIPSearchAPI
    """
    DEFAULT_TIMEFRAME = 90
    DATE_FORMAT = "%Y-%m-%d %H:%M"
    TIMEDELTA_DEFAULT_TIMEFRAME = datetime.timedelta(days=DEFAULT_TIMEFRAME)

    def __init__(self, query, query_count=None):
        self.api_request = self.api()
        self.timeframe = self.request_timeframe()
        self.query = query
        self.query_count = query_count
        self.interval = "hour"
        # TODO: FIX THIS
        self.days = self.timeframe.days
        self.start = self.timeframe.start
        self.end = self.timeframe.end

    def request_timeframe(self):
        """
        Returns a timeframe to use in the API query
        """
        request_timeframe = Timeframe(start=None, end=None, interval="hour")
        return request_timeframe

    def api(self):
        """
        Returns GNIPSearchAPI
        """
        return GnipSearchAPI(required_environment('GNIP_USER_NAME'),
                             required_environment('GNIP_PASSWORD'),
                             required_https_endpoint('GNIP_SEARCH_ENDPOINT'),
                             paged=False)

    def get_timeline(self):
        """
        Returns a timeline of tweets e.g. Date > Tweet Count etc.
        """
        timeline = None
        try:
            timeline = self.api().query_api(
                pt_filter=str(
                    self.query),
                max_results=0,
                use_case="timeline",
                start=self.timeframe.start.strftime(
                    self.DATE_FORMAT),
                end=self.timeframe.end.strftime(
                    self.DATE_FORMAT),
                count_bucket=self.timeframe.interval,
                csv_flag=False)
        except GNIPQueryError as e:
            print e

        return timeline

    def get_tweets(self):
        """
        Returns tweets in a list object
        """
        if (self.timeframe.start < datetime.datetime.now() -
            self.timeframe.TIMEDELTA_DEFAULT_TIMEFRAME) and (self.timeframe.start +
                                                             self.timeframe.TIMEDELTA_DEFAULT_TIMEFRAME > self.timeframe.end):
            end = self.timeframe.start + self.timeframe.TIMEDELTA_DEFAULT_TIMEFRAME
        query_nrt = self.query
        not_rt = "-(is:retweet)"
        if (not_rt not in query_nrt):
            query_nrt = query_nrt.replace("is:retweet", "")
            query_nrt = "%s %s" % (query_nrt, not_rt)
        tweets = None
        try:
            tweets = self.api().query_api(
                query_nrt,
                self.query_count,
                use_case="tweets",
                start=self.timeframe.start.strftime(
                    self.DATE_FORMAT),
                end=self.timeframe.end.strftime(
                    self.DATE_FORMAT))
        except GNIPQueryError as e:
            print e
            return None
        return tweets
