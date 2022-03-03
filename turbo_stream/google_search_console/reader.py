"""
Google Search Console API
"""
import logging

from turbo_stream import ReaderInterface
import os
import pickle
import time

import googleapiclient
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import OAuth2WebServerFlow

from turbo_stream.utils.date_handlers import date_range
from turbo_stream.utils.file_handlers import un_nest_keys
from turbo_stream.utils.request_handlers import request_handler

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO
)


class GoogleSearchConsoleReader(ReaderInterface):
    """
    Google Search Console API Reader
    """

    def __init__(self, configuration: dict, credentials: (dict, str), **kwargs):
        super().__init__(configuration, credentials)

        self.scopes = kwargs.get(
            "scopes",
            (
                "https://www.googleapis.com/auth/webmasters.readonly",
                "https://www.googleapis.com/auth/webmasters",
            ),
        )
        self.discovery_uri = kwargs.get(
            "discovery_uri",
            ("https://www.googleapis.com/discovery/v1/apis/customsearch/v1/rest"),
        )
        self.oauth_scope = kwargs.get(
            "oath_scope", "https://www.googleapis.com/auth/webmasters.readonly"
        )
        self.redirect_uri = kwargs.get("redirect_uri", "urn:ietf:wg:oauth:2.0:oob")

    def generate_authentication(
        self, auth_file_location="gsc_credentials.pickle"
    ) -> None:
        """
        A user friendly method to generate a .pickle file for future authentication.
        For the first time, you would need to log in with your web browser based on
        this web authentication flow. After that, it will save your credentials in
        a pickle file. Every subsequent time you run the script, it will use the
        “pickled” credentials stored in credentials.pickle to build the
        connection to Search Console.
        """
        flow = OAuth2WebServerFlow(
            self._credentials["installed"].get("client_id"),
            self._credentials["installed"].get("client_secret"),
            self.oauth_scope,
            self.redirect_uri,
        )
        authorize_url = flow.step1_get_authorize_url()
        logging.info(f"Go to the following link in your browser: {authorize_url}")
        code = input("Enter verification code: ").strip()
        credentials = flow.step2_exchange(code)
        pickle.dump(credentials, open(auth_file_location, "wb"))

    def _get_service(self) -> build:
        """
        Makes use of the .pickle cred file to establish a webmaster connection.
        """
        credentials = pickle.load(open(self._credentials, "rb"))
        return build("webmasters", "v3", credentials=credentials, cache_discovery=False)

    @request_handler(wait=1, backoff_factor=0.5)
    def _query_handler(self, service, request, site_url):
        """
        Run the API request that consumes a request payload and site url.
        This separates the request with the request handler from the rest of the logic.
        """
        logging.info(f"Querying for Site Url: {site_url}.")
        return service.searchanalytics().query(siteUrl=site_url, body=request).execute()

    def run_query(self):
        """
        Consumes a .yaml config file and loops through the date and url
        to return relevant data from GSC API.
        """
        service = self._get_service()
        start_date = self._configuration.get("startDate")
        end_date = self._configuration.get("endDate")

        # split request by date to reduce 504 errors
        for date in date_range(start_date=start_date, end_date=end_date):
            # run until none is returned or there is no more data in rows
            row_index = 0
            while True:
                request = {
                    "startDate": date,
                    "endDate": date,
                    "dimensions": self._configuration.get("dimensions"),
                    "metrics": self._configuration.get("metrics"),
                    "searchType": self._configuration.get("searchType"),
                    "rowLimit": self._configuration.get("maxRows", 25000),
                    "startRow": row_index * self._configuration.get("maxRows", 25000),
                    "aggregationType": self._configuration.get(
                        "aggregationType", "byPage"
                    ),
                }

                try:
                    response = self._query_handler(
                        service=service,
                        request=request,
                        site_url=self._configuration.get("siteUrl"),
                    )

                    if response is None:
                        logging.info("Response is None, stopping.")
                        break
                    if "rows" not in response:
                        logging.info("No more data in Response.")
                        break

                    # added additional data that the api does not provide
                    # un un_nest keys
                    for row in response["rows"]:
                        row["site_url"] = self._configuration.get("siteUrl")
                        row["search_type"] = self._configuration.get("searchType")
                        row = un_nest_keys(
                            data=row,
                            col="keys",
                            key_list=self._configuration.get("dimensions"),
                            value_list=row.get("keys"),
                        )
                        self._append_data_set(row)
                    row_index += 1

                except googleapiclient.errors.HttpError as error:
                    if error.resp.status == 403:
                        message = (
                            f"GSC quotaExceeded on: {self._configuration.get('siteUrl')} "
                            f"for {self._configuration.get('searchType')}, "
                            f"waiting for 15 minutes."
                        )
                        logging.info(message)
                        time.sleep(900)
                    else:
                        raise error

        return self._data_set
