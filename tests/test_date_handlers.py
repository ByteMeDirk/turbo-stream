"""
Test turbo_stream.utils.date_handlers
"""
import unittest
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from turbo_stream.utils.date_handlers import phrase_to_date, _is_integer, date_range

DATE_FORMAT = "%Y-%m-%d"


class TestDateHandlers(unittest.TestCase):
    """
    Testing the Date Handlers.
    """

    def test_phrase_to_date_today(self):
        """
        Test the phrase_to_date method with phrase today.
        """
        _date = phrase_to_date("today", DATE_FORMAT)
        self.assertEqual(_date, (datetime.now()).strftime(DATE_FORMAT))

    def test_phrase_to_date_yesterday(self):
        """
        Test the phrase_to_date method with phrase yesterday.
        """
        _date = phrase_to_date("yesterday", DATE_FORMAT)
        self.assertEqual(
            _date, (datetime.now() - timedelta(days=1)).strftime(DATE_FORMAT)
        )

    def test_phrase_to_date_day(self):
        """
        Test the phrase_to_date method with a stream of day phrases.
        """
        for day in range(1, 1000):
            _date = phrase_to_date(f"{day}_days_ago", DATE_FORMAT)
            self.assertEqual(
                _date, (datetime.now() - timedelta(days=day)).strftime(DATE_FORMAT)
            )

    def test_phrase_to_date_month(self):
        """
        Test the phrase_to_date method with a stream of month phrases.
        """
        for day in range(1, 100):
            _date = phrase_to_date(f"{day}_months_ago", DATE_FORMAT)
            self.assertEqual(
                _date,
                (datetime.now() - relativedelta(months=day)).strftime(DATE_FORMAT),
            )

    def test_phrase_to_date_week(self):
        """
        Test the phrase_to_date method with a stream of week phrases.
        """
        for day in range(1, 100):
            _date = phrase_to_date(f"{day}_weeks_ago", DATE_FORMAT)
            self.assertEqual(
                _date, (datetime.now() - relativedelta(weeks=day)).strftime(DATE_FORMAT)
            )

    def test_phrase_to_date_year(self):
        """
        Test the phrase_to_date method with a stream of year phrases.
        """
        for day in range(1, 10):
            _date = phrase_to_date(f"{day}_years_ago", DATE_FORMAT)
            self.assertEqual(
                _date, (datetime.now() - relativedelta(years=day)).strftime(DATE_FORMAT)
            )

    def test_is_integer(self):
        """
        Test the phrase_to_date _is_integer private method.
        """
        self.assertEqual(_is_integer("5"), True)
        self.assertEqual(_is_integer(5), True)
        self.assertEqual(_is_integer(5.0), True)
        self.assertEqual(_is_integer("five"), False)

    def test_date_range(self):
        """
        Test the date_range method.
        """
        date_list = []
        for date in date_range("2022-01-01", "2022-01-05"):
            date_list.append(date)

        self.assertEqual(
            date_list,
            ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04", "2022-01-05"],
        )
