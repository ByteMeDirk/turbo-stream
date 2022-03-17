"""
Test turbo_stream.utils.file_handlers
"""
import os
import unittest

from turbo_stream.utils.file_handlers import load_file, write_file


class TestFileHandlers(unittest.TestCase):
    """
    Test turbo_stream.utils.file_handlers
    """

    def test_load_file_json(self):
        """
        Test if file_loader successfully loads a json file.
        """
        self.assertEqual(
            load_file("tests/assets/config.json", "json"),
            {"test_config": {"key": "value"}},
        )

    def test_load_file_yml(self):
        """
        Test if file_loader successfully loads a yml file.
        """
        self.assertEqual(
            load_file("tests/assets/config.yml", "yml"),
            {"test_config": {"key": "value"}},
        )

    def test_load_file_yaml(self):
        """
        Test if file_loader successfully loads a yaml file.
        """
        self.assertEqual(
            load_file("tests/assets/config.yaml", "yaml"),
            {"test_config": {"key": "value"}},
        )

    def test_write_file_yml(self):
        """
        Test if writer successfully writes to yml file.
        """
        write_file(data={"test_config": {"key": "value"}}, file_location="test.yml")
        self.assertTrue(os.path.isfile("test.yml"))
        os.remove("test.yml")

    def test_write_file_yaml(self):
        """
        Test if writer successfully writes to yaml file.
        """
        write_file(data={"test_config": {"key": "value"}}, file_location="test.yaml")
        self.assertTrue(os.path.isfile("test.yaml"))
        os.remove("test.yaml")

    def test_write_file_json(self):
        """
        Test if writer successfully writes to json file.
        """
        write_file(data={"test_config": {"key": "value"}}, file_location="test.json")
        self.assertTrue(os.path.isfile("test.json"))
        os.remove("test.json")

    def test_write_file_csv(self):
        """
        Test if writer successfully writes to csv file.
        """
        write_file(data={"test_config": {"key": "value"}}, file_location="test.csv")
        self.assertTrue(os.path.isfile("test.csv"))
        os.remove("test.csv")
