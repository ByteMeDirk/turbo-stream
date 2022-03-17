"""
Google Search Console API
"""
import logging
import pickle
from socket import timeout

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import OAuth2WebServerFlow

from turbo_stream import ReaderInterface, write_file, write_file_to_s3
from turbo_stream.utils.date_handlers import date_range
from turbo_stream.utils.request_handlers import request_handler, retry_handler

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
        with open(self._credentials, "rb") as _file:
            credentials = pickle.load(_file)

        return build(
            "searchconsole", "v1", credentials=credentials, cache_discovery=False
        )

    @request_handler(wait=1, backoff_factor=0.5)
    @retry_handler(
        exceptions=(timeout, HttpError),
        total_tries=5,
        initial_wait=60,
        backoff_factor=5,
    )
    def _query_handler(self, service, request, site_url):
        """
        Run the API request that consumes a request payload and site url.
        This separates the request with the request handler from the rest of the logic.
        """
        return service.searchanalytics().query(siteUrl=site_url, body=request).execute()

    def run_query(self):
        """
        Consumes a .yaml config file and loops through the date and url
        to return relevant data from GSC API.
        """
        service: build = self._get_service()
        start_date: str = self._configuration.get("start_date")
        end_date: str = self._configuration.get("end_date")
        dimensions: list = self._configuration.get("dimensions")

        logging.info(
            f"Gathering data between given dates {start_date} and {end_date}. "
            f"Querying for Site Url: {self._configuration.get('site_url')}."
        )

        dimension_data_set = {}
        # split request by date to reduce 504 errors
        for dimension in dimensions:
            for date in date_range(start_date=start_date, end_date=end_date):
                logging.info(f"Querying at date: {date} for dimension: {dimension}.")
                # run until none is returned or there is no more data in rows
                row_index = 0
                while True:
                    dim_query_set = list(dict.fromkeys(["date", dimension]))
                    response = self._query_handler(
                        service=service,
                        request={
                            "startDate": date,
                            "endDate": date,
                            "dimensions": dim_query_set,
                            "metrics": self._configuration.get("metrics"),
                            "type": self._configuration.get("type"),
                            "rowLimit": self._configuration.get("row_limit", 25000),
                            "startRow": row_index
                            * self._configuration.get("row_limit", 25000),
                            "aggregationType": self._configuration.get(
                                "aggregation_type", "auto"
                            ),
                            "dimensionFilterGroups": self._configuration.get(
                                "dimension_filter_groups", []
                            ),
                            "dataState": self._configuration.get("data_state", "final"),
                        },
                        site_url=self._configuration.get("site_url"),
                    )

                    if response is None:
                        logging.info("Response is None, exiting process...")
                        break
                    if "rows" not in response:
                        logging.info("No more data in given row, moving on....")
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
                                    dim_query_set,
                                    row.get("keys", []),
                                )
                            )
                        )

                        # get metrics data
                        for metric in self._configuration.get("metrics", []):
                            dataset[metric] = row.get(metric)

                        if dimension not in dimension_data_set:
                            dimension_data_set[dimension] = []
                        dimension_data_set[dimension].append(dataset)
                    row_index += 1

            self._append_data_set(dimension_data_set)

        logging.info(f"{self.__class__.__name__} process complete!")
        return self._data_set

    def write_date_to_local(self, file_location):
        """
        GSC returns queries for each dimension respectively. The response data is
        response_dataset = {
         "date": ["dimension response data"],
         "page": ["dimension response data"],
         "query": ["dimension response data"]
        }
        So each dimension will be written as its own dataset to local.
        :param file_location:  Local file location.
        """
        for dimension, dimension_dataset in self._data_set[0].items():
            file_split = file_location.split(".")
            filepath = f"{file_split[0]}_{dimension}.{file_split[-1]}"
            logging.info(f"Writing {dimension} data to local path: {filepath}.")
            write_file(data=dimension_dataset, file_location=filepath)

    def write_partition_data_to_s3(
        self, bucket: str, path: str, partition: str, fmt="json"
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
        for dimension, dimension_dataset in self._data_set[0].items():
            partition_dataset = self._partition_dataset(
                partition=partition, dataset=dimension_dataset
            )
            for partition_name, partition_data in partition_dataset.items():
                write_file_to_s3(
                    bucket=bucket,
                    key=f"{path}/{partition_name}_{dimension}.{fmt}",
                    data=partition_data,
                )
