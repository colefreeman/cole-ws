from google.cloud import bigquery
import os
from typing import Any


@data_exporter
def main(data: Any, *args, **kwargs):
    """
    Load transformed data into BigQuery table.

    Args:
        data (Any): The data to be loaded into BigQuery.
        kwargs (dict): Additional keyword arguments if needed.
    """

    # Initialize BigQuery client
    project_id: str = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable is not set.")

    client: bigquery.Client = bigquery.Client(project=project_id)

    # Define dataset and table name
    dataset_id: str = os.environ.get("BIGQUERY_DATASET_ID")
    table_id: str = os.environ.get("BIGQUERY_TABLE_NAME")
    if not dataset_id or not table_id:
        raise ValueError(
            "Environment variables BIGQUERY_DATASET_ID and BIGQUERY_TABLE_NAME must be set."
        )

    table_ref: bigquery.TableReference = client.dataset(dataset_id).table(table_id)

    # Prepare data for insertion
    # Assuming data is a list of dictionaries
    if not isinstance(data, list):
        raise TypeError("Data should be a list of dictionaries.")

    # Insert data into BigQuery
    errors: list = client.insert_rows_json(table_ref, data)

    if errors:
        # Handle insertion errors
        raise RuntimeError(f"Failed to insert rows into BigQuery: {errors}")

    # Confirm successful insertion
    print(f"Successfully inserted {len(data)} rows into {dataset_id}.{table_id}.")
