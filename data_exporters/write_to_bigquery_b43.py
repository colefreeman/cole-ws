from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os


@data_exporter
def main(df: pd.DataFrame, *args, **kwargs):
    """
    Write the transformed weather DataFrame into a BigQuery table.
    Uses service account credentials from environment variables or mounted secret file.
    """

    # Define your BigQuery dataset and table name
    dataset_id = os.getenv("BIGQUERY_DATASET", "your_dataset_name")
    table_id = os.getenv("BIGQUERY_TABLE", "your_table_name")

    # Path to the service account key file, set via environment variable or mounted secret
    key_path = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "/path/to/your/service-account-key.json"
    )

    # Create credentials object
    credentials = service_account.Credentials.from_service_account_file(key_path)

    # Initialize BigQuery client
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # Define the full table ID
    full_table_id = f"{client.project}.{dataset_id}.{table_id}"

    # Write DataFrame to BigQuery, append mode
    client.load_table_from_dataframe(
        df,
        full_table_id,
        job_config=bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            # Optionally, specify schema if needed:
            # schema=[bigquery.SchemaField("name", "STRING"), ...],
        ),
    ).result()  # Wait for the job to complete
