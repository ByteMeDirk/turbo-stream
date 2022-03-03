"""
Test turbo_stream.utils.file_handlers
"""
import unittest

from turbo_stream.utils.file_handlers import load_file


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
