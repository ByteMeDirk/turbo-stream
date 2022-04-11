import re


def snake_case_string(field: str, replace: tuple = None) -> str:
    """
    Converts any CamelCase string into snake_case with the added functionality
    to replace a string.
    :param field: The string object to be converted.
    :param replace: Optional set of two values where value 0 will be replaced with value 1 in the field string.
    :return: The snake_case string.
    """
    if replace is None:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", field).lower()

    # if replace is not none, make sure it is a valid set
    if replace is not None and len(replace) != 2:
        raise ValueError(
            "Replace param only consumes one set of two values for the replace method."
        )

    return re.sub(
        r"(?<!^)(?=[A-Z])", "_", field.replace(replace[0], replace[1])
    ).lower()
