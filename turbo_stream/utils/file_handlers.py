"""
File Handler Methods
"""
import json
import logging

import pandas as pd
import yaml

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO
)


def load_file(file_location: str, fmt: str) -> dict:
    """
    Gathers file data from json or yaml.
    """
    if fmt in ["yaml", "yml"]:
        with open(file_location, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)

    if fmt == "json":
        with open(file_location, "r", encoding="utf-8") as file:
            return json.load(file)

    raise ValueError(f"fmt {fmt} is not supported, try yaml, yml or json.")


def write_file(data: (dict, list), file_location):
    """
    Writes object to json, csv or yaml.
    """
    fmt = file_location.split(".")[-1]

    if fmt in ["yaml", "yml"]:
        with open(file_location, "w", encoding="utf-8") as file:
            file.write(yaml.dump(data, sort_keys=False))

    elif fmt == "json":
        with open(file_location, "w", encoding="utf-8") as file:
            file.write(json.dumps(data))

    elif fmt == "csv":
        try:
            df = pd.DataFrame(data)
            df.to_csv(file_location, header=True, index=True)
        except ValueError as err:
            df = pd.DataFrame(list(data))
            df.to_csv(file_location, header=True, index=True)

    else:
        raise ValueError(f"fmt {fmt} is not supported, try yaml, yml, csv or json.")
