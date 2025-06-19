import os
from typing import Any
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


@data_exporter
def main(
    df: pd.DataFrame,
    **kwargs: Any,
) -> None:
    """
    Export the cleaned Titanic dataset to a BigQuery table.

    Args:
        df (pd.DataFrame): Cleaned Titanic dataset with standardized headers.
        **kwargs: Additional keyword arguments for configuration, such as:
            - project_id (str): GCP project ID.
            - dataset_id (str): BigQuery dataset ID.
            - table_id (str): BigQuery table name.
            - gcp_credentials_path (str, optional): Path to GCP service account JSON key file.

    Returns:
        None
    """

    # Retrieve configuration from kwargs or environment variables
    project_id: str = kwargs.get('project_id') or os.getenv('GCP_PROJECT_ID')
    dataset_id: str = kwargs.get('dataset_id') or os.getenv('BQ_DATASET_ID')
    table_id: str = kwargs.get('table_id') or os.getenv('BQ_TABLE_ID')
    gcp_credentials_path: str = kwargs.get('gcp_credentials_path') or os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    if not all([project_id, dataset_id, table_id]):
        raise ValueError("Missing required BigQuery configuration: project_id, dataset_id, or table_id.")

    # Set up BigQuery client with optional service account credentials
    if gcp_credentials_path:
        credentials = service_account.Credentials.from_service_account_file(gcp_credentials_path)
        client = bigquery.Client(project=project_id, credentials=credentials)
    else:
        client = bigquery.Client(project=project_id)

    # Construct the full table ID in standard SQL format
    full_table_id: str = f"{project_id}.{dataset_id}.{table_id}"

    # Define job configuration for BigQuery load
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # Overwrite table if exists
        autodetect=True,  # Let BigQuery auto-detect the schema
    )

    # Upload the DataFrame to BigQuery
    job = client.load_table_from_dataframe(
        df,
        full_table_id,
        job_config=job_config,
    )

    # Wait for the job to complete
    job.result()

    # Optionally, you could check the table after upload (not required)
    # table = client.get_table(full_table_id)
    # print(f"Loaded {table.num_rows} rows to {full_table_id}")



# No test functions are required since the main function returns None.
