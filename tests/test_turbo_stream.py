"""
Test turbo_stream.Reader
"""
import unittest

import botocore
import boto3
import pytest
from moto import mock_s3

from turbo_stream import ReaderInterface

MOCK_PAYLOAD = {"key": "value"}
S3_CLIENT = boto3.client("s3")


class TestTurboStream(unittest.TestCase):
    """
    Test turbo_stream.Reader
    """

    def test_fun_intro(self):
        """
        Test the get_configuration method.
        """
        reader = ReaderInterface(
            configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD, intro_off=False
        )
        self.assertEqual(reader.get_configuration(), MOCK_PAYLOAD)

    def test_get_configuration(self):
        """
        Test the get_configuration method.
        """
        reader = ReaderInterface(
            configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD, intro_off=True
        )
        self.assertEqual(reader.get_configuration(), MOCK_PAYLOAD)

    def test_get_credentials(self):
        """
        Test the get_credentials method.
        """
        reader = ReaderInterface(
            configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD, intro_off=True
        )
        self.assertEqual(reader.get_credentials(), MOCK_PAYLOAD)

    def test_set_configuration(self):
        """
        Test the set_configuration method.
        """
        reader = ReaderInterface(
            configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD, intro_off=True
        )
        reader.set_configuration({"key1": "value1"})
        self.assertEqual(reader.get_configuration(), {"key1": "value1"})

    def test_set_credentials(self):
        """
        Test the set_credentials method.
        """
        reader = ReaderInterface(
            configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD, intro_off=True
        )
        reader.set_credentials({"key1": "value1"})
        self.assertEqual(reader.get_credentials(), {"key1": "value1"})

    def test_set_dataset(self):
        """
        Test the _set_data_set method.
        """
        reader = ReaderInterface(
            configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD, intro_off=True
        )
        reader._set_data_set([{"key1": "value1"}])
        self.assertEqual(reader._data_set, [{"key1": "value1"}])

    def test_append_dataset(self):
        """
        Test the set_credentials method.
        """
        reader = ReaderInterface(
            configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD, intro_off=True
        )
        reader._append_data_set({"key0": "value0"})
        reader._append_data_set({"key1": "value1"})
        self.assertEqual(reader._data_set, [{"key0": "value0"}, {"key1": "value1"}])

    def test_partition_dataset(self):
        """
        Test partition functionality when writing to s3
        """
        reader = ReaderInterface(
            configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD, intro_off=True
        )
        reader._data_set = [
            {"date": "2021-01-01", "value": 15},
            {"date": "2021-01-02", "value": 16},
        ]
        self.assertEqual(
            reader._partition_dataset("date"),
            {
                "2021-01-01": [{"date": "2021-01-01", "value": 15}],
                "2021-01-02": [{"date": "2021-01-02", "value": 16}],
            },
        )

    @mock_s3
    def test_write_partition_data_to_s3(self):
        """
        Test write functionality when writing to s3.
        """
        with pytest.raises(Exception):
            reader = ReaderInterface(
                configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD, intro_off=True
            )
            reader._data_set = [
                {"date": "2021-01-01", "value": 15},
                {"date": "2021-01-02", "value": 16},
            ]
            reader.write_partition_data_to_s3(
                bucket="test", path="test", partition="date"
            )

    @mock_s3
    def test_write_data_to_s3(self):
        """
        Test write functionality when writing to s3.
        """
        with pytest.raises(Exception):
            reader = ReaderInterface(
                configuration=MOCK_PAYLOAD, credentials=MOCK_PAYLOAD, intro_off=True
            )
            reader._data_set = [
                {"date": "2021-01-01", "value": 15},
                {"date": "2021-01-02", "value": 16},
            ]
            reader.write_data_to_s3(bucket="test", key="test.json")
