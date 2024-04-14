## Purpose

We have two different sources of data, both available through an API:
- sales data
- product usage data

Implement the project to:
1- fetch this data using the api
2- store it in BigQuery
3- build a KPI on top of it

The api can be reached at this url: "https://7znsvl36xuuuky0qezgn.lambda-url.eu-central-1.on.aws/"
It requires 3 params:
- kind that can be either "sales" or "product_usage" depending on the kind of data you are looking for
- api_version. Current version is "1.0"
- day with a format "yyy-mm-dd". For exemple March 1st 2023 will be provided as "2023-03-01"
The time range is limited to March 2023.

To authenticate to BigQuery you will use the provided service account.

To store data you will use the following dataset_id: "business-operations-361115.bi_engineer_test_ayoussoufi".

The KPI we expect is the sum of all deal that were signed up to a given day.
You can create a table with two column: day and kpi_value and fill it for every day of March.
