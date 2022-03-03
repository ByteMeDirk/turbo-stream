"""
File Handler Methods
"""
import json
import logging

import yaml

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO
)


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
