"""
Google Search Console API
"""
import logging
import pickle

from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

from turbo_stream import ReaderInterface
from turbo_stream.utils.date_handlers import date_range
from turbo_stream.utils.request_handlers import request_handler


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
        start_date = self._configuration.get("start_date")
        end_date = self._configuration.get("end_date")
        logging.info(f"Gathering data between given dates {start_date} and {end_date}.")

        # split request by date to reduce 504 errors
        for date in date_range(start_date=start_date, end_date=end_date):
            # run until none is returned or there is no more data in rows
            row_index = 0
            while True:
                response = self._query_handler(
                    service=service,
                    request={
                        "startDate": date,
                        "endDate": date,
                        "dimensions": self._configuration.get("dimensions"),
                        "metrics": self._configuration.get("metrics"),
                        "searchType": self._configuration.get("search_type"),
                        "rowLimit": self._configuration.get("row_limit", 25000),
                        "startRow": row_index
                        * self._configuration.get("row_limit", 25000),
                        "aggregationType": self._configuration.get(
                            "aggregation_type", "auto"
                        ),
                    },
                    site_url=self._configuration.get("site_url"),
                )

                if response is None:
                    logging.info("Response is None, stopping.")
                    break
                if "rows" not in response:
                    logging.info("No more data in Response.")
                    break

                # added additional data that the api does not provide
                for row in response["rows"]:
                    dataset = {
                        "site_url": self._configuration.get("site_url"),
                        "search_type": self._configuration.get("search_type"),
                    }

                    # get dimension data keys and values
                    dataset.update(
                        dict(
                            zip(
                                self._configuration.get("dimensions", []),
                                row.get("keys", []),
                            )
                        )
                    )

                    # get metrics data
                    for metric in self._configuration.get("metrics", []):
                        dataset[metric] = row.get(metric)

                    self._append_data_set(dataset)
                row_index += 1

        return self._data_set
