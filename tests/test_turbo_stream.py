"""
Test turbo_stream.Reader
"""
import unittest

from turbo_stream import Reader

MOCK_PAYLOAD = {"key": "value"}
READER = Reader(configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD)


class TestTurboStream(unittest.TestCase):
    """
    Test turbo_stream.Reader
    """

    def test_get_configuration(self):
        """
        Test the get_configuration method.
        """
        self.assertEqual(READER.get_configuration(), MOCK_PAYLOAD)

    def test_get_credentials(self):
        """
        Test the get_credentials method.
        """
        self.assertEqual(READER.get_credentials(), MOCK_PAYLOAD)
