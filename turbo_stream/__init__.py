"""
Turbo Stream Interfaces
"""

import logging

from .utils.aws_handlers import write_file_to_s3
from .utils.file_handlers import write_file

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO
)

_intro_flag = (
    "|\nWelcome to:                                                             \n"
    "@+####################################################################+@\n"
    "@+ _____            _                 __ _                            +@\n"
    "@+/__   \\_   _ _ __| |__   ___       / _\\ |_ _ __ ___  __ _ _ __ ___  +@\n"
    "@+  / /\\/ | | | '__| '_ \\ / _ \\ _____\\ \\| __| '__/ _ \\/ _` | '_ ` _ \\+@\n"
    "@+ / /  | |_| | |  | |_) | (_) |_____|\\ \\ |_| | |  __/ (_| | | | | | |+@\n"
    "@+ \\/    \\__,_|_|  |_.__/ \\___/      \\__/\\__|_|  \\___|\\__,_|_| |_| |_|+@\n"
    "@+--------------------------------------------------------------------+@\n"
    "@+ It is dangerous to go alone, take this...                          +@\n"
    "@+                         \\    /\\                                    +@\n"
    "@+                          )  ( ')    < meow...                      +@\n"
    "@+                         (  /  )                                    +@\n"
    "@+                          \\(__)|                                    +@\n"
    "@+####################################################################+@\n"
    "                                                             By: DirksCGM\n"
)


class ReaderInterface:
    """
    Turbo Stream Reader Class Interface
    """

    def __init__(self, configuration: dict, credentials: (dict, str), **kwargs):
        self._configuration: dict = configuration
        self._credentials: (dict, str) = credentials
        self._data_set: list = []

        self.profile_name = kwargs.get("profile_name")

        if not kwargs.get("intro_off", True):
            # A fun intro banner for the service log
            logging.info(
                _intro_flag
            )

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

    def get_data_set(self) -> list:
        """
        :return: Returns whole dataset object.
        """
        return self._data_set

    def _append_data_set(self, row: dict) -> None:
        """
        Append key-value pair to dataset object.
        :param row: single key-value pair.
        :return: None
        """
        self._data_set.append(row)

    def _partition_dataset(self, partition: str, dataset=None) -> dict:
        """
        Returns an object where the data is sorted by the keys as partitions, and
        the values relating to the given keys. THe partitions are essentially fields in
        the dataset that become partitioned within the data.
        :param partition: The field name in the dataset what will become the partition.
        :return: Partitioned object.
        """
        # provide the option to modify the class method write object
        if dataset is None:
            dataset = self._data_set

        partition_dataset = {}
        for row in dataset:
            date_value = row.get(partition)
            if date_value not in partition_dataset:
                partition_dataset[date_value] = []
            partition_dataset[date_value].append(row)

        return partition_dataset

    def write_partition_data_to_local(
            self, path: str, partition: str, fmt="parquet"
    ):
        """
        Writes a file to local, partitioned by a given field in the dataset.
        Json objects will be serialised before writing. This works best with date fields
        where the use-case would be to reduce duplicates stored.
        Specifying the file type in the name will serialise the data.Supported formats are
        Json, CSV, Parquet and Text.
        :param path: The path in the bucket where the partition file will be written.
        :param partition: The field name in the dataset what will become the partition.
        :param fmt: The format to write in.
        :return: The partitioned dataset object
        """
        partition_dataset = self._partition_dataset(partition=partition)
        for partition_name, partition_data in partition_dataset.items():
            write_file(
                file_location=f"{path}/{partition_name}.{fmt}", data=partition_data
            )

    def write_partition_data_to_s3(
            self, bucket: str, path: str, partition: str, fmt="parquet"
    ):
        """
        Writes a file to s3, partitioned by a given field in the dataset.
        Json objects will be serialised before writing. This works best with date fields
        where the use-case would be to reduce duplicates stored in s3.
        Specifying the file type in the name will serialise the data.Supported formats are
        Json, CSV, Parquet and Text.
        :param bucket: The bucket to write to in s3.
        :param path: The path in the bucket where the partition file will be written.
        :param partition: The field name in the dataset what will become the partition.
        :param fmt: The format to write in.
        :return: The partitioned dataset object
        """
        partition_dataset = self._partition_dataset(partition=partition)
        for partition_name, partition_data in partition_dataset.items():
            write_file_to_s3(
                bucket=bucket, key=f"{path}/{partition_name}.{fmt}", data=partition_data
            )

    def write_data_to_s3(self, bucket: str, key: str):
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

    def write_date_to_local(self, file_location):
        """
        Writes data object to local file as json, csv or yaml.
        :param file_location: Local file location.
        """
        logging.info(f"Writing data to local path: {file_location}.")
        write_file(data=self._data_set, file_location=file_location)
