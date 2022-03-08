"""
Turbo Stream Interfaces
"""
import logging
from datetime import datetime

from .utils.aws_handlers import write_file_to_s3

_LOG_FILE_NAME = f"turbo_stream_{datetime.utcnow()}.log"


def _set_up_logging() -> None:
    """
    Set up file and stream handler for loggging globally.
    """
    log_format = logging.Formatter(
        "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    )
    root_logger = logging.getLogger()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)


class ReaderInterface:
    """
    Turbo Stream Reader Class Interface
    """

    def __init__(self, configuration: dict, credentials: (dict, str), **kwargs):
        self._configuration: dict = configuration
        self._credentials: (dict, str) = credentials
        self._data_set: list = []

        self.profile_name = kwargs.get("profile_name")

        _set_up_logging()

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

    def write_data_to_s3(self, bucket, key):
        """
        Writes a file to s3. Json objects will be serialised before writing.
        Specifying the file type in the name will serialise the data.Supported formats are
        Json, CSV, Parquet and Text.
        :param bucket: The bucket to write to in s3.
        :param key: The key path and filename where the data will be stored.
        """
        write_file_to_s3(
            bucket=bucket, key=key, data=self._data_set, profile_name=self.profile_name
        )
