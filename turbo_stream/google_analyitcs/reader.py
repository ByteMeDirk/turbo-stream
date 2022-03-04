"""
Google Analytics V3 Core Reporting API
"""
import logging
from socket import timeout

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

from turbo_stream import ReaderInterface
from turbo_stream.utils.date_handlers import phrase_to_date
from turbo_stream.utils.request_handlers import request_handler, retry_handler


class GoogleAnalyticsV3Reader(ReaderInterface):
    """
    Google Analytics V3 Core Reporting API Reader
    """

    def __init__(
        self,
        configuration: dict,
        credentials: str,
        service_account_email: str,
        **kwargs,
    ):
        super().__init__(configuration, credentials)

        # google analytics expects a path to a .p12 file
        self._credentials = credentials

        self.service_account_email = service_account_email
        self.scopes = kwargs.get(
            "scopes", ["https://www.googleapis.com/auth/analytics.readonly"]
        )

    def _get_service(self) -> build:
        """
        Get a service that communicates to the Google V3 Core Reporting API.
        """
        credentials = ServiceAccountCredentials.from_p12_keyfile(
            filename=self._credentials,
            scopes=self.scopes,
            service_account_email=self.service_account_email,
        )
        return build(
            serviceName="analytics",
            version="v3",
            credentials=credentials,
            cache_discovery=False,
        )

    @staticmethod
    def _normalize_data(report) -> list:
        """
        Flattens the response data to a standard dict.
        """
        headers = [head["name"] for head in report["columnHeaders"]]
        profile = report["profileInfo"]

        data_set = []
        for row in report["rows"]:
            tmp = dict(zip(headers, row))
            tmp.update(profile)
            data_set.append(tmp)

        return data_set

    @request_handler(wait=1, backoff_factor=0.5)
    @retry_handler(
        exceptions=(timeout, HttpError),
        total_tries=5,
        initial_wait=60,
        backoff_factor=5,
    )
    def _query_handler(self, property_id, service, start_index):
        """
        Separated query method to handle retry and delay methods.
        """

        start_date = phrase_to_date(self._configuration.get("start_date"))
        end_date = phrase_to_date(self._configuration.get("end_date"))
        logging.info(f"Gathering data between given dates {start_date} and {end_date}.")
        response = (
            service.data()
            .ga()
            .get(
                ids=f"ga:{property_id}",
                start_date=start_date,
                end_date=end_date,
                # convert mets and dims into comma separated string
                metrics=",".join(self._configuration.get("metrics", [])),
                dimensions=",".join(self._configuration.get("dimensions", [])),
                sort=self._configuration.get("sort", None),
                filters=self._configuration.get("filters", None),
                max_results=self._configuration.get("max_results", 10000),
                start_index=start_index,
                samplingLevel=self._configuration.get(
                    "sampling_level", "HIGHER_PRECISION"
                ),
                include_empty_rows=self._configuration.get("include_empty_rows", True),
            )
        )
        return response.execute()

    def run_query(self):
        """
        Core V3 Reporting API.
        The method will try each query 5 times before failing.
        Config File:
            start_date: |
              Start date for fetching Analytics data.
              Requests can specify a start date formatted as YYYY-MM-DD,
              or as a relative date (e.g., today, yesterday, or
              NdaysAgo where N is a positive integer).
            end_date: |
              End date for fetching Analytics data.
              Request can specify an end date formatted as YYYY-MM-DD,
              or as a relative date (e.g., today, yesterday, or
              NdaysAgo where N is a positive integer).
            metrics: A maximum of 10 Metrics in list form.
            dimensions: A maximum of 7 Dimensions in list form.
            sort: |
              A list of comma-separated dimensions and metrics
              indicating the sorting order and sorting direction for the returned data.
            filters: Dimension or metric filters that restrict the data returned for your request.
            property_ids: |
              A list of the unique table ID of the form ga:XXXX, where XXXX is the
              Analytics view (profile) ID for which the query will retrieve the data.
        """
        for property_id in self._configuration.get("property_ids"):
            service = self._get_service()  # new service for each view_id
            page_token = 1  # handle paging of response
            while True:
                logging.info(
                    f"Querying for Property Id: {property_id} at Page Token: {page_token}."
                )
                response = self._query_handler(
                    service=service, property_id=property_id, start_index=page_token
                )
                if len(response.get("rows", [])) < 1:
                    logging.info(
                        f"No more data for Property Id: {property_id} at Page Token: {page_token}."
                    )
                    break
                page_token += response.get("itemsPerPage", 0)

                for row in self._normalize_data(response):
                    self._append_data_set(row)

        return self._data_set
