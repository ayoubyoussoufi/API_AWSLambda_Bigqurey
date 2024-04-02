import requests
from google.cloud import bigquery
from datetime import datetime, timedelta
from google.api_core.exceptions import NotFound
import pandas as pd
import json

# Load the service account credentials from the JSON file
credentials_dict = json.load(open("business-operations-361115-50b55c4c1b70_ayoussoufi.json"))

# Define constants
API_URL = "https://7znsvc5o3765l6x6ml36xuuuky0qezgn.lambda-url.eu-central-1.on.aws/"
DATASET_ID = "bi_engineer_test_ayoussoufi"
API_VERSION = "1.0"


def fetch_data(kind, day):
    params = {
        "kind": kind,
        "api_version": API_VERSION,
        "day": day
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch {kind} data for {day}. Status code: {response.status_code}")
        return None


def store_data_in_bigquery(df, table_name, credentials_dict, dataset_id=DATASET_ID):
    client = bigquery.Client.from_service_account_info(credentials_dict)
    dataset_ref = client.dataset(dataset_id)

    # Check if the dataset exists, if not, create it
    try:
        dataset = client.get_dataset(dataset_ref)
        print(f"Dataset '{dataset_id}' already exists.")
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        try:
            client.create_dataset(dataset)
            print(f"Dataset '{dataset_id}' created successfully.")
        except Exception as e:
            print(f"Error creating dataset: {e}")

    table_ref = dataset_ref.table(table_name)

    # Check if the table exists, if not, create it
    try:
        table = client.get_table(table_ref)
        print(f"Table '{table_name}' already exists.")
    except NotFound:
        schema = [bigquery.SchemaField(name, 'STRING') for name in df.columns]
        table = bigquery.Table(table_ref, schema=schema)
        try:
            client.create_table(table)
            print(f"Table '{table_name}' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")

    # Insert rows from DataFrame into the table
    errors = client.insert_rows_from_dataframe(table, df)

    if errors == []:
        print(f"Data inserted successfully into {table_name} table.")
    else:
        print(f"Errors occurred while inserting data into {table_name} table: {errors}")


def calculate_kpi(sales_data):
    kpi_data = []

    # Iterate through each day's data
    for idx, sales_day in enumerate(sales_data, 1):
        # Initialize the total sales value for the day
        total_sales_value = 0

        # Check if sales_day is not None and not empty
        if sales_day is not None and sales_day:
            # Iterate through each deal in the sales data
            for deal in sales_day:
                # Extract the amount and add it to the total sales value
                total_sales_value += deal.get("amount", 0)
            # Append the day index and the total sales value to kpi_data
            kpi_data.append({"day": f"2023-03-{str(idx).zfill(2)}", "kpi_value": total_sales_value})
        else:
            # Append the day index with kpi_value as None
            kpi_data.append({"day": f"2023-03-{str(idx).zfill(2)}", "kpi_value": None})

    return kpi_data


def main():
    # Fetch data for March 2023
    start_date = datetime(2023, 3, 1)
    end_date = datetime(2023, 3, 31)
    delta = timedelta(days=1)
    dates = []
    sales_data = []
    product_usage_data = []
    while start_date <= end_date:
        dates.append(start_date.strftime("%Y-%m-%d"))
        sales_data.append(fetch_data("sales", start_date.strftime("%Y-%m-%d")))
        product_usage_data.append(fetch_data("product_usage", start_date.strftime("%Y-%m-%d")))
        start_date += delta
    # Flatten the sales and product_usage_data
    flattened_sales_data = [item for sublist in sales_data if sublist is not None for item in sublist]
    flattened_product_usage_data = [item for sublist in product_usage_data if sublist is not None for item in sublist]
    sales_data_df = pd.DataFrame(flattened_sales_data)
    product_usage_data_df = pd.DataFrame(flattened_product_usage_data)

    # Store KPI data in BigQuery
    store_data_in_bigquery(sales_data_df, "sales_data", credentials_dict)
    store_data_in_bigquery(product_usage_data_df, "product_usage_data", credentials_dict)

    # calculate KPI
    kpi_data = calculate_kpi(sales_data)
    kpi_data_df = pd.DataFrame(kpi_data)
    store_data_in_bigquery(kpi_data_df, "result_data", credentials_dict)


if __name__ == "__main__":
    main()
