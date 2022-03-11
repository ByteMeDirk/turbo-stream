"""
Test turbo_stream.google_analytics.reader
"""
import unittest

import OpenSSL
import pytest
from googleapiclient.discovery import build

from turbo_stream.google_analyitcs.reader import GoogleAnalyticsReader


class TestGoogleAnalyticsReader(unittest.TestCase):
    """
    Test turbo_stream.google_analytics.reader
    """

    def test_set_credentials(self):
        """
        Tests if the class gathers the credentials.
        """
        reader = GoogleAnalyticsReader(
            credentials="tests/assets/mock_ga_creds.p12",
            configuration={},
            service_account_email="",
        )

        self.assertEqual(reader._credentials, "tests/assets/mock_ga_creds.p12")
        self.assertEqual(reader.get_credentials(), "tests/assets/mock_ga_creds.p12")

    def test_set_configs(self):
        """
        Tests if the class gathers the configs.
        """
        reader = GoogleAnalyticsReader(
            credentials="", configuration={}, service_account_email=""
        )

        self.assertEqual(reader._configuration, {})
        self.assertEqual(reader.get_configuration(), {})

    def test_get_service(self):
        """
        Tests if the GA build object connects.
        """
        reader = GoogleAnalyticsReader(
            credentials="tests/assets/mock_ga_creds.p12",
            configuration={},
            service_account_email="",
        )

        with pytest.raises(OpenSSL.crypto.Error):
            reader._get_service()

    def test_query_handler(self):
        """
        Test if query handler fetches service.
        """
        reader = GoogleAnalyticsReader(
            credentials="tests/assets/mock_ga_creds.p12",
            configuration={"start_date": "today", "end_date": "today"},
            service_account_email="",
        )

        with pytest.raises(AttributeError):
            reader._query_handler("123456", build, "2022-01-01")

    def test_run_query(self):
        """
        Test if query handler fetches service.
        """
        reader = GoogleAnalyticsReader(
            credentials="tests/assets/mock_ga_creds.p12",
            configuration={"start_date": "today", "end_date": "today"},
            service_account_email="",
        )

        with pytest.raises(TypeError):
            reader.run_query()
