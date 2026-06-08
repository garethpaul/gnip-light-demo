import datetime
import unittest

from gnip_search.timeframe import Timeframe


class TimeframeTest(unittest.TestCase):

    def test_explicit_dates_are_parsed_and_counted(self):
        timeframe = Timeframe(
            start="2026-01-01 00:00",
            end="2026-01-04 12:00",
            interval="hour",
        )

        self.assertEqual(datetime.datetime(2026, 1, 1, 0, 0), timeframe.start)
        self.assertEqual(datetime.datetime(2026, 1, 4, 12, 0), timeframe.end)
        self.assertEqual("hour", timeframe.interval)
        self.assertEqual(3, timeframe.days)

    def test_inverted_dates_use_default_lookback_days(self):
        timeframe = Timeframe(
            start="2026-02-01 00:00",
            end="2026-01-01 00:00",
            interval="day",
        )

        self.assertEqual(datetime.datetime(2026, 1, 1, 0, 0), timeframe.end)
        self.assertEqual(timeframe.end - Timeframe.TIMEDELTA_DEFAULT_TIMEFRAME, timeframe.start)
        self.assertEqual(Timeframe.DEFAULT_TIMEFRAME, timeframe.days)


if __name__ == "__main__":
    unittest.main()
