"""
Turbo Stream Interfaces
"""
import logging

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO
)


class ReaderInterface:
    """
    Turbo Stream Reader Class Interface
    """

    def __init__(self, configuration: dict, credentials: (dict, str)):
        self._configuration: dict = configuration
        self._credentials: (dict, str) = credentials
        self._data_set: list = []

    def get_configuration(self) -> dict:
        """
        :return: Returns configuration object.
        """
        return self._configuration

    def get_credentials(self) -> dict:
        """
        :return: Returns credentials object.
        """
        return self._credentials

    def set_configuration(self, configuration: dict) -> None:
        """
        Set configuration object.
        :param configuration: dict configuration object that matches the vendor requirements.
        :return: None
        """
        self._configuration = configuration

    def set_credentials(self, credentials: dict) -> None:
        """
        Set credentials object.
        :param credentials: dict credentials object that matches the vendor requirements.
        :return: None
        """
        self._credentials = credentials

    def _set_data_set(self, data_set: list) -> None:
        """
        Set whole dataset object, overwriting the original one.
        :param data_set: list of key-value pairs.
        :return: None
        """
        self._data_set = data_set

    def _append_data_set(self, row: dict) -> None:
        """
        Append key-value pair to dataset object.
        :param row: single key-value pair.
        :return: None
        """
        self._data_set.append(row)
