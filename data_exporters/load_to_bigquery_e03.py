from google.cloud import bigquery
from typing import Any
from data_exporter import get_secret_value
from google.oauth2 import service_account
from your_secrets_manager_module import get_secret_value


@data_exporter
def main(input_data: Any, *args, **kwargs):
    """
    Load the transformed weather data into BigQuery table 'weather_data' in the specified dataset.
    Assumes input_data is a DataFrame with columns: 'timestamp', 'temperature_f', 'humidity_percent'.
    """

    # Retrieve BigQuery credentials path from secrets manager
    credentials_path: str = get_secret_value("GCP_CRED_FILE")

    # Initialize BigQuery client with service account credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )
    client = bigquery.Client(credentials=credentials)

    # Define dataset and table name
    dataset_id: str = "your_dataset_name"  # Replace with your dataset name
    table_id: str = "weather_data"

    # Construct full table ID
    full_table_id: str = f"{client.project}.{dataset_id}.{table_id}"

    # Convert input DataFrame to list of dictionaries
    # Assuming input_data is a pandas DataFrame
    data_as_dicts: list = input_data.to_dict(orient="records")

    # Load data into BigQuery
    # Use load_table_from_json for streaming insert
    errors = client.load_table_from_json(
        json_rows=data_as_dicts,
        destination=full_table_id,
        job_config=bigquery.LoadJobConfig(
            schema=[
                bigquery.SchemaField("timestamp", "TIMESTAMP"),
                bigquery.SchemaField("temperature_f", "FLOAT"),
                bigquery.SchemaField("humidity_percent", "FLOAT"),
            ],
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        ),
    ).result()

    # Optionally, handle errors
    if errors:
        raise RuntimeError(f"BigQuery load errors: {errors}")

    # No return needed as per specification
