"""
File Handler Methods
"""
import json
import logging

import yaml

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO
)


def un_nest_keys(data, col, key_list, value_list):
    """
    A simple method that takes a set of keys and values
    from a dataset with dimensions and replaces them
    with key value pairs.

    :data: The dataset that needs to be un_nested.
    :col: The key name of the dimensions.
    :key_list: List of keys.
    :value_list: List of Values.

    returns:
        So dataset A:
            {'keys': [1, 2, 3]}
        Can become:
            {'key1': 1, 'key2': 2, 'key3': 3}
    """
    data.update(dict(zip(key_list, value_list)))
    del data[col]
    return data


def load_file(file_location: str, fmt: str) -> dict:
    """
    Gathers file data from json or yaml.
    """
    if file_location is not None:
        if fmt in ["yaml", "yml"]:
            with open(file_location, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        elif fmt == "json":
            with open(file_location, "r", encoding="utf-8") as file:
                return json.load(file)
