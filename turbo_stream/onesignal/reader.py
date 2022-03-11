"""
Onesignal API
"""
import logging
import time
from urllib.error import URLError

import pandas as pd
import requests

from turbo_stream import ReaderInterface
from turbo_stream.utils.file_handlers import load_file
from turbo_stream.utils.request_handlers import request_handler, retry_handler

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO
)


class OnesignalReader(ReaderInterface):
    """
    Onesignal API Reader for View Notifications and CSV Exports.
    """

    def __init__(self, configuration: dict, credentials: (dict, str), **kwargs):
        super().__init__(configuration, credentials)

        # load credentials file to object
        self._credentials = load_file(
            file_location=credentials, fmt=kwargs.get("credential_file_fmt", "yml")
        )

        self._app_id = self._credentials.get("app_id")
        self._api_key = self._credentials.get("api_key")
        self._header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {self._api_key}",
        }

        self._csv_wait_time = kwargs.get("csv_wait_time", 30)
        self._csv_get_attempts = kwargs.get("csv_get_attempts", 5)

    def _generate_url(self, endpoint: str):
        """
        Generate url string for authentication from given endpoints.
        :param endpoint: view_notification or csv_export
        :return: Url string.
        """
        if endpoint == "view_notification":
            return f"https://onesignal.com/api/v1/notifications?app_id={self._app_id}"
        if endpoint == "csv_export":
            return (
                f"https://onesignal.com/api/v1/players/csv_export?app_id={self._app_id}"
            )

        raise ValueError(
            f"Given endpoint: {endpoint} is not supported. "
            f"Try csv_export or view_notifications."
        )

    @request_handler(wait=0.5, backoff_factor=0.5)
    def _view_notification_query_handler(self, limit: int, offset: int):
        url = self._generate_url(endpoint="view_notification")
        return requests.get(
            url=url,
            headers=self._header,
            params={"limit": limit, "total_count": "true", "offset": offset},
        )

    @request_handler(wait=1, backoff_factor=0.5)
    def _csv_export_query_handler(self):
        url = self._generate_url(endpoint="csv_export")
        return requests.post(url=url, headers=self._header)

    def run_query(self):
        """
        Generate a compressed CSV export of all of your current user data.
        This method can be used to generate a compressed CSV export of all of your current user data.
        View the details of multiple notifications.
        :return: The response dataset.
        """
        _endpoint = self._configuration.get("endpoint")
        _limit = self._configuration.get("limit", 50)
        logging.info(f"Gathering data for {_endpoint}.")

        if _endpoint == "view_notification":
            # gather data per offset given the set of limits
            initial_response = self._view_notification_query_handler(
                limit=_limit, offset=0
            ).json()
            _total_records = int(initial_response.get("total_count"))

            for offset in range(0, _total_records, _limit):
                logging.info(f"At offset {offset} of {_total_records}.")
                response = self._view_notification_query_handler(
                    limit=_limit, offset=offset
                ).json()
                self._data_set.append(response)

            logging.info(f"{self.__class__.__name__} process complete!")
            return self._data_set

        if _endpoint == "csv_export":
            response = self._csv_export_query_handler().json()
            csv_url = response.get("csv_file_url", None)

            # if connection is good, try to get the csv file from the Onesignal
            # Athena wrapper, it could take time to generate, so wait for it.
            if csv_url is not None:
                attempts = 1
                while True:
                    try:
                        logging.info(f"Attempting to gather data from url: {csv_url}.")
                        data_frame: pd.DataFrame = pd.read_csv(csv_url)
                        self._data_set = data_frame.to_dict(orient="records")
                        logging.info("Data gathered, decompressing and serialising...")

                        logging.info(f"{self.__class__.__name__} process complete!")
                        return self._data_set

                    except URLError:
                        logging.info(
                            f"CSV file not generated, waiting for {self._csv_wait_time} seconds. "
                            f"Attempt {attempts}/{self._csv_get_attempts}."
                        )
                        time.sleep(self._csv_wait_time)
                        if attempts > self._csv_get_attempts:
                            logging.info(
                                "CSV file failed to generate after 10 attempts. "
                                "Contact Onesignal for help."
                            )
                        attempts += 1
            else:
                raise ConnectionError(response)

        raise ValueError(
            f"Given endpoint: {_endpoint} is not supported. "
            f"Try csv_export or view_notifications."
        )
