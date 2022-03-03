"""main"""
from turbo_stream.google_analyitcs.reader import GoogleAnalyticsV3Reader


def main():
    """stuff"""
    reader = GoogleAnalyticsV3Reader(
        configuration={
            "start_date": "today",
            "end_date": "today",
            "metrics": ["ga:pageviews"],
            "dimensions": ["ga:date", "ga:medium", "ga:pagePath"],
            "property_ids": ["184192516", "108383162"],
        },
        credentials="search-and-data-249754da0457.p12",
        service_account_email="pipelines@search-and-data.iam.gserviceaccount.com",
    )

    data = reader.run_query()

    print(data)


if __name__ == "__main__":
    main()
