"""
Test turbo_stream.google_search_console.reader
"""
import unittest

import OpenSSL
import pytest
from googleapiclient.discovery import build

from turbo_stream.google_search_console.reader import GoogleSearchConsoleReader


class TestGoogleSearchConsoleReader(unittest.TestCase):
    """
    Test turbo_stream.google_search_console.reader
    """

    def test_set_credentials(self):
        """
        Tests if the class gathers the credentials.
        """
        reader = GoogleSearchConsoleReader(
            credentials="tests/assets/mock_gsc_creds.pickle",
            configuration={},
            intro_off=True,
        )

        self.assertEqual(reader._credentials, "tests/assets/mock_gsc_creds.pickle")
        self.assertEqual(reader.get_credentials(), "tests/assets/mock_gsc_creds.pickle")

    def test_set_configs(self):
        """
        Tests if the class GoogleSearchConsoleReader the configs.
        """
        reader = GoogleSearchConsoleReader(
            credentials={}, configuration={}, intro_off=True
        )

        self.assertEqual(reader._configuration, {})
        self.assertEqual(reader.get_configuration(), {})

    def test_generate_authentication(self):
        """
        Tests if the GSC build object attempts.
        """
        reader = GoogleSearchConsoleReader(
            credentials="tests/assets/mock_gsc_creds.json",
            configuration={},
            intro_off=True,
        )

        with pytest.raises(TypeError):
            reader.generate_authentication()

    def test_get_service(self):
        """
        Tests if the GSC service object connects.
        """
        reader = GoogleSearchConsoleReader(
            credentials="tests/assets/mock_gsc_creds.pickle",
            configuration={},
            intro_off=True,
        )

        with pytest.raises(EOFError):
            reader._get_service()

    def test_query_handler(self):
        """
        Test if query handler fetches service.
        """
        reader = GoogleSearchConsoleReader(
            credentials="tests/assets/mock_gsc_creds.pickle",
            configuration={"start_date": "today", "end_date": "today"},
            intro_off=True,
        )

        with pytest.raises(EOFError):
            reader._query_handler(reader._get_service(), "", "")

    def test_run_query(self):
        """
        Test if query attempts to run.
        """
        reader = GoogleSearchConsoleReader(
            credentials="tests/assets/mock_gsc_creds.pickle",
            configuration={"start_date": "today", "end_date": "today"},
            intro_off=True,
        )

        with pytest.raises(EOFError):
            reader.run_query()
