"""
Test turbo_stream.utils.file_handlers
"""
import unittest

from turbo_stream.utils.file_handlers import load_file, un_nest_keys


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

    def test_un_nest_data(self):
        """
        Test the unnest method.
        """
        self.assertEqual(
            un_nest_keys(
                data={"keys": [1, 2]},
                col="keys",
                key_list=["key1", "key2"],
                value_list=[1, 2, 3, 4],
            ),
            {"key1": 1, "key2": 2},
        )
