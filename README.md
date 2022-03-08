# turbo-stream

A module for down-streaming data from a selection of vendors.

[![tests](https://github.com/DirksCGM/turbo-stream/actions/workflows/tests.yml/badge.svg)](https://github.com/DirksCGM/turbo-stream/actions/workflows/tests.yml)
[![publish to pypi](https://github.com/DirksCGM/turbo-stream/actions/workflows/publish.yml/badge.svg)](https://github.com/DirksCGM/turbo-stream/actions/workflows/publish.yml)
![PyPI](https://img.shields.io/pypi/v/turbo_stream)
![PyPI - Downloads](https://img.shields.io/pypi/dm/turbo_stream)

## Google Analytics Core v3 Reporting Api

### Configuration

configuration object:

```json
{
  "property_ids": [
    "xxxxxxxxx"
  ],
  "start_date": "5_days_ago",
  "end_date": "today",
  "metrics": [
    "ga:xxx"
  ],
  "dimensions": [
    "ga:xxx"
  ],
  "sort": "",
  "filters": "",
  "max_results": 10000,
  "sampling_level": "HIGHER_PRECISION",
  "include_empty_rows": true
}
```

### Example

```python
from turbo_stream.google_analyitcs.reader import GoogleAnalyticsV3Reader


def main():
    reader = GoogleAnalyticsV3Reader(
        configuration={},
        credentials="xxx.p12",
        service_account_email="xxx@xxx.com",
    )

    reader.run_query()
    reader.write_data_to_s3(bucket="xxx", key="xx/x.json")


if __name__ == "__main__":
    main()
```

## Google Search Console Api

### Generate Credentials.pickle for GSC Api:

A user-friendly method to generate a .pickle file for future authentication is available in the reader as
the `generate_authentication()` method. For the first time, you would need to log in with your web browser based on this
web authentication flow. After that, it will save your credentials in a pickle file. Every subsequent time you run the
script, it will use the “pickled” credentials stored in credentials.pickle to build the connection to Search Console.

```python
from turbo_stream.google_search_console.reader import GoogleSearchConsoleReader


def main():
    reader = GoogleSearchConsoleReader(
        configuration={},
        credentials="google_search_console_creds.json"  # to generate, make use of the secrets.json
    )

    reader.generate_authentication(auth_file_location="google_search_console_creds.pickle")


if __name__ == "__main__":
    main()
```

### Configuration

configuration object:

```json
{
  "start_date": "5_days_ago",
  "end_date": "today",
  "dimensions": [],
  "metrics": [],
  "searchType": "",
  "rowLimit": 25000,
  "siteUrl": "https://www.xxx.com/",
  "aggregation_type": "byPage"
}
```

### Example

```python
from turbo_stream.google_search_console.reader import GoogleSearchConsoleReader


def main():
    reader = GoogleSearchConsoleReader(
        configuration={},
        credentials="google_search_console_creds.pickle"
    )

    reader.run_query()
    reader.write_data_to_s3(bucket="xxx", key="xx/x.json")


if __name__ == "__main__":
    main()
```

## Writing Partitions to s3

Writes a file to s3, partitioned by a given field in the dataset. Json objects will be serialised before writing. This
works best with date fields where the use-case would be to reduce duplicates stored in s3. Specifying the file type in
the name will serialise the data.Supported formats are Json, CSV, Parquet and Text.

```python
from turbo_stream.google_analyitcs.reader import GoogleAnalyticsV3Reader


def main():
    reader = GoogleAnalyticsV3Reader(
        configuration={},
        credentials="xxx.p12",
        service_account_email="xxx@xxx.com",
    )

    reader.run_query()
    reader.write_partition_data_to_s3(bucket="xxx", path="xx", partition="date")


if __name__ == "__main__":
    main()
```
