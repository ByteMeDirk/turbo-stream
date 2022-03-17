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
            intro_off=True,
        )

        self.assertEqual(reader._credentials, "tests/assets/mock_ga_creds.p12")
        self.assertEqual(reader.get_credentials(), "tests/assets/mock_ga_creds.p12")

    def test_set_configs(self):
        """
        Tests if the class gathers the configs.
        """
        reader = GoogleAnalyticsReader(
            credentials="", configuration={}, service_account_email="", intro_off=True
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
            intro_off=True,
        )

        with pytest.raises(OpenSSL.crypto.Error):
            reader._get_service()

    def test_iterate_report(self):
        """
        Test if iterator returns a refined dataset.
        """
        reader = GoogleAnalyticsReader(
            credentials="tests/assets/mock_ga_creds.p12",
            configuration={},
            service_account_email="",
            intro_off=True,
        )

        reader._iterate_report(
            reports=[
                {
                    "columnHeader": {
                        "dimensions": ["ga:date"],
                        "metricHeader": {
                            "metricHeaderEntries": [
                                {"name": "ga:users", "type": "INTEGER"},
                                {"name": "ga:sessions", "type": "INTEGER"},
                            ]
                        },
                    },
                    "data": {
                        "rows": [
                            {
                                "dimensions": ["20010101"],
                                "metrics": [{"values": ["1000", "1000"]}],
                            }
                        ],
                        "totals": [{"values": ["1000", "1000"]}],
                        "rowCount": 1,
                        "minimums": [{"values": ["1000", "1000"]}],
                        "maximums": [{"values": ["1000", "1000"]}],
                        "dataLastRefreshed": "2001-01-01T01:01:01Z",
                    },
                }
            ],
            view_id="0000",
        )

        self.assertEqual(
            reader._data_set,
            [
                {
                    "ga:date": "20010101",
                    "ga:users": 1000,
                    "ga:sessions": 1000,
                    "ga:viewId": "0000",
                }
            ],
        )

    def test_query_handler(self):
        """
        Test if query handler fetches service.
        """
        reader = GoogleAnalyticsReader(
            credentials="tests/assets/mock_ga_creds.p12",
            configuration={"start_date": "today", "end_date": "today"},
            service_account_email="",
            intro_off=True,
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
            intro_off=True,
        )

        with pytest.raises(TypeError):
            reader.run_query()
