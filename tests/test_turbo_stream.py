"""
Test turbo_stream.Reader
"""
import unittest

import pytest
from botocore.exceptions import ClientError, NoCredentialsError

from turbo_stream import ReaderInterface

MOCK_PAYLOAD = {"key": "value"}


class TestTurboStream(unittest.TestCase):
    """
    Test turbo_stream.Reader
    """

    def test_get_configuration(self):
        """
        Test the get_configuration method.
        """
        reader = ReaderInterface(configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD)
        self.assertEqual(reader.get_configuration(), MOCK_PAYLOAD)

    def test_get_credentials(self):
        """
        Test the get_credentials method.
        """
        reader = ReaderInterface(configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD)
        self.assertEqual(reader.get_credentials(), MOCK_PAYLOAD)

    def test_set_configuration(self):
        """
        Test the set_configuration method.
        """
        reader = ReaderInterface(configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD)
        reader.set_configuration({"key1": "value1"})
        self.assertEqual(reader.get_configuration(), {"key1": "value1"})

    def test_set_credentials(self):
        """
        Test the set_credentials method.
        """
        reader = ReaderInterface(configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD)
        reader.set_credentials({"key1": "value1"})
        self.assertEqual(reader.get_credentials(), {"key1": "value1"})

    def test_set_dataset(self):
        """
        Test the _set_data_set method.
        """
        reader = ReaderInterface(configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD)
        reader._set_data_set([{"key1": "value1"}])
        self.assertEqual(reader._data_set, [{"key1": "value1"}])

    def test_append_dataset(self):
        """
        Test the set_credentials method.
        """
        reader = ReaderInterface(configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD)
        reader._append_data_set({"key0": "value0"})
        reader._append_data_set({"key1": "value1"})
        self.assertEqual(reader._data_set, [{"key0": "value0"}, {"key1": "value1"}])

    def test_write_data_to_s3(self):
        """
        Test the access of the boto3 s3 witer method.
        """
        reader = ReaderInterface(configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD)
        with pytest.raises(ClientError, NoCredentialsError):
            reader.write_data_to_s3(bucket="test", key="test.json")
