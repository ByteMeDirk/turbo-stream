# turbo-stream

A module for down-streaming data from a selection of vendors.

[![tests](https://github.com/DirksCGM/turbo-stream/actions/workflows/tests.yml/badge.svg)](https://github.com/DirksCGM/turbo-stream/actions/workflows/tests.yml)
[![publish to pypi](https://github.com/DirksCGM/turbo-stream/actions/workflows/publish.yml/badge.svg)](https://github.com/DirksCGM/turbo-stream/actions/workflows/publish.yml)

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

