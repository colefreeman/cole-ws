import os
import pandas as pd
from azure.storage.blob import BlobServiceClient


@data_exporter
def export_data(
    data: "pd.DataFrame",
    **kwargs,
) -> None:
    """
    Export the transformed DataFrame to the target storage system.
    """

    # Retrieve Azure Blob Storage connection string from environment variables
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")
    blob_name = os.getenv("TARGET_BLOB_NAME")

    # Validate input data
    if data is None or not isinstance(data, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame.")

    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Convert DataFrame to CSV bytes
    csv_bytes = data.to_csv(index=False).encode("utf-8")

    # Upload the CSV to Azure Blob Storage
    try:
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )
        blob_client.upload_blob(csv_bytes, overwrite=True)
    except Exception as e:
        raise RuntimeError(f"Failed to upload data to Azure Blob Storage: {e}")
