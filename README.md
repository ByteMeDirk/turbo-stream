# turbo-stream

A module for down-streaming data from a selection of vendors.

[![tests](https://github.com/DirksCGM/turbo-stream/actions/workflows/tests.yml/badge.svg)](https://github.com/DirksCGM/turbo-stream/actions/workflows/tests.yml)

## Google Analytics Core v3 Reporting Api

configuration object:

```json
{
  "start_date": "5_days_ago",
  "end_date": "today",
  "metrics": [
    "ga:xxx"
  ],
  "dimensions": [
    "ga:xxx",
  ],
  "property_ids": [
    "xxxxxxxxx",
  ]
}
```
