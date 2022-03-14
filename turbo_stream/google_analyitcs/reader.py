"""
Google Analytics V3 Core Reporting API
"""
import logging
from socket import timeout

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

from turbo_stream import ReaderInterface
from turbo_stream.utils.date_handlers import phrase_to_date, date_range
from turbo_stream.utils.request_handlers import request_handler, retry_handler

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO
)


class GoogleAnalyticsReader(ReaderInterface):
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
            version="v4",
            credentials=credentials,
            cache_discovery=False,
            discoveryServiceUrl='https://analyticsreporting.googleapis.com/$discovery/rest'
        )

    @request_handler(wait=1, backoff_factor=0.5)
    @retry_handler(
        exceptions=(timeout, HttpError),
        total_tries=5,
        initial_wait=60,
        backoff_factor=5,
    )
    def _query_handler(self, view_id, service, date):
        """
        Separated query method to handle retry and delay methods.
        """
        logging.info(f"Querying at date: {date}.")

        metrics_set = []
        for metric in self._configuration.get("metrics", []):
            metrics_set.append({"expression": metric})

        dimensions_set = []
        for dimension in self._configuration.get("dimensions", []):
            dimensions_set.append({"name": dimension})

        response = service.reports().batchGet(
            body={
                "reportRequests": [
                    {
                        "viewId": view_id,
                        "dateRanges": [{"startDate": date, "endDate": date}],
                        "metrics": metrics_set,
                        "dimensions": dimensions_set,
                        "metricFilterClauses": self._configuration.get(
                            "metric_filter_clauses", []
                        ),
                        "dimensionFilterClauses": self._configuration.get(
                            "dimension_filter_clauses", []
                        ),
                        "filtersExpression": self._configuration.get("filters_expression"),
                        "orderBys": self._configuration.get("order_bys", []),
                        "samplingLevel": self._configuration.get("sampling_level", "LARGE"),
                        "includeEmptyRows": self._configuration.get("include_empty_rows", "true"),
                    }
                ]
            }
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
        start_date = phrase_to_date(self._configuration.get("start_date"))
        end_date = phrase_to_date(self._configuration.get("end_date"))
        for view_id in self._configuration.get("view_ids"):
            logging.info(f"Querying data for View Id: {view_id}.")
            service = self._get_service()  # new service for each view_id
            for date in date_range(start_date=start_date, end_date=end_date):
                response = self._query_handler(
                    view_id=view_id, service=service, date=date
                )
                for report in response.get("reports", []):
                    column_header = report.get("columnHeader", {})
                    dimension_headers = column_header.get("dimensions", [])
                    metric_headers = column_header.get("metricHeader", {}).get(
                        "metricHeaderEntries", []
                    )

                    for row in report.get("data", {}).get("rows", []):
                        # create dict for each row
                        row_dict = {}
                        dimensions = row.get("dimensions", [])
                        date_range_values = row.get("metrics", [])

                        for header, dimension in zip(dimension_headers, dimensions):
                            row_dict[header] = dimension

                        # ToDo: Unused variable "i"
                        for i, values in enumerate(date_range_values):
                            for metric, value in zip(
                                metric_headers, values.get("values")
                            ):
                                # clean up ints and floats
                                if "," in value or "." in value:
                                    row_dict[metric.get("name")] = float(value)
                                else:
                                    row_dict[metric.get("name")] = int(value)

                        # add additional data
                        row_dict["ga:viewId"] = view_id

                        self._data_set.append(row_dict)

        logging.info(f"{self.__class__.__name__} process complete!")
        return self._data_set
