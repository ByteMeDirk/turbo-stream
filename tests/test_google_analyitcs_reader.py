"""
Test turbo_stream.google_analytics.reader
"""
import unittest

import OpenSSL
import pytest
from googleapiclient.discovery import build

from turbo_stream.google_analyitcs.reader import GoogleAnalyticsV3Reader


class TestGoogleAnalyticsV3Reader(unittest.TestCase):
    """
    Test turbo_stream.google_analytics.reader
    """

    def test_set_credentials(self):
        """
        Tests if the class gathers the credentials.
        """
        reader = GoogleAnalyticsV3Reader(
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
        reader = GoogleAnalyticsV3Reader(
            credentials="", configuration={}, service_account_email=""
        )

        self.assertEqual(reader._configuration, {})
        self.assertEqual(reader.get_configuration(), {})

    def test_get_service(self):
        """
        Tests if the GA build object connects.
        """
        reader = GoogleAnalyticsV3Reader(
            credentials="tests/assets/mock_ga_creds.p12",
            configuration={},
            service_account_email="",
        )

        with pytest.raises(OpenSSL.crypto.Error):
            reader._get_service()

    def test_normalize_data(self):
        """
        Tests the normalisation of the GA reader class-method.
        """
        reader = GoogleAnalyticsV3Reader(
            credentials="tests/assets/mock_ga_creds.p12",
            configuration={},
            service_account_email="",
        )

        mock_report_string = {
            "kind": "analytics#gaData",
            "id": "xxxxxx",
            "query": {
                "start-date": "2022-03-04",
                "end-date": "2022-03-04",
                "ids": "ga:xxxxxx",
                "dimensions": "ga:date,ga:medium,ga:pagePath",
                "metrics": ["ga:pageviews"],
                "start-index": 2,
                "max-results": 1,
                "samplingLevel": "HIGHER_PRECISION",
            },
            "itemsPerPage": 1,
            "totalResults": 1,
            "selfLink": "xxxxxx",
            "previousLink": "xxxxxx",
            "nextLink": "xxxxxx",
            "profileInfo": {
                "profileId": "xxxxxx",
                "accountId": "xxxxxx",
                "webPropertyId": "UA-xxxxxx3-1",
                "internalWebPropertyId": "xxxxxx",
                "profileName": "mock reporting view",
                "tableId": "ga:xxxxxx",
            },
            "containsSampledData": False,
            "dataLastRefreshed": "1646000000",
            "columnHeaders": [
                {"name": "ga:date", "columnType": "DIMENSION", "dataType": "STRING"},
                {"name": "ga:medium", "columnType": "DIMENSION", "dataType": "STRING"},
                {
                    "name": "ga:pagePath",
                    "columnType": "DIMENSION",
                    "dataType": "STRING",
                },
                {"name": "ga:pageviews", "columnType": "METRIC", "dataType": "INTEGER"},
            ],
            "totalsForAllResults": {"ga:pageviews": "xxxxx"},
            "rows": [["xxxxxx", "xxxxxx", "xxxxxx", "xxxxxx"]],
        }
        self.assertEqual(
            reader._normalize_data(mock_report_string),
            [
                {
                    "ga:date": "xxxxxx",
                    "ga:medium": "xxxxxx",
                    "ga:pagePath": "xxxxxx",
                    "ga:pageviews": "xxxxxx",
                    "profileId": "xxxxxx",
                    "accountId": "xxxxxx",
                    "webPropertyId": "UA-xxxxxx3-1",
                    "internalWebPropertyId": "xxxxxx",
                    "profileName": "mock reporting view",
                    "tableId": "ga:xxxxxx",
                }
            ],
        )

    def test_query_handler(self):
        """
        Test if query handler fetches service.
        """
        reader = GoogleAnalyticsV3Reader(
            credentials="tests/assets/mock_ga_creds.p12",
            configuration={"start_date": "today", "end_date": "today"},
            service_account_email="",
        )

        with pytest.raises(AttributeError):
            reader._query_handler("123456", build, 1)

    def test_run_query(self):
        """
        Test if query handler fetches service.
        """
        reader = GoogleAnalyticsV3Reader(
            credentials="tests/assets/mock_ga_creds.p12",
            configuration={"start_date": "today", "end_date": "today"},
            service_account_email="",
        )

        with pytest.raises(TypeError):
            reader.run_query()
