import os
from azure.storage.blob import BlobServiceClient
import pandas as pd


@data_loader
def load_data_322() -> pd.DataFrame:
    """
    Loads data from Azure Blob Storage for initial data ingestion.
    """

    # Retrieve Azure Storage connection string from environment variables
    connection_string: str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not connection_string:
        raise ValueError(
            "Azure Storage connection string not found in environment variables."
        )

    # Specify the container name and blob name
    container_name: str = os.getenv("AZURE_CONTAINER_NAME")
    blob_name: str = os.getenv("AZURE_BLOB_NAME")
    if not container_name or not blob_name:
        raise ValueError(
            "Container name or blob name not found in environment variables."
        )

    # Initialize the BlobServiceClient
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(
        connection_string
    )

    # Get the BlobClient for the specific blob
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )

    # Download the blob data as bytes
    download_stream = blob_client.download_blob()
    blob_bytes: bytes = download_stream.readall()

    # Convert bytes to string assuming CSV format; adjust if different format
    data_str: str = blob_bytes.decode("utf-8")

    # Read the CSV data into a pandas DataFrame using StringIO
    df: pd.DataFrame = pd.read_csv(pd.compat.StringIO(data_str))

    return df
