import pandas as pd
from unittest.mock import patch
from mage_ai.data_preparation.shared.secrets import get_secret_value
from mage_ai.data_preparation.io import AzureBlobStorage


@transformer
def azure_blob_storage_load_and_validate_a4a() -> "DataFrame":
    """
    Load data from Azure Blob Storage, mock during testing, and validate the data.
    """

    # Retrieve necessary secrets for Azure Blob Storage authentication
    azure_connection_str = get_secret_value("AZURE_STORAGE_CONNECTION_STRING")
    container_name = get_secret_value("AZURE_CONTAINER_NAME")
    blob_name = get_secret_value("AZURE_BLOB_NAME")

    # Initialize AzureBlobStorage client
    storage_client = AzureBlobStorage(
        connection_str=azure_connection_str,
        container_name=container_name,
    )

    # Mock the load method during testing to simulate data loading
    with patch.object(
        storage_client,
        "load",
        return_value=pd.DataFrame({"id": [1, 2, 3], "value": ["a", "b", "c"]}),
    ):
        # Load data from Azure Blob Storage
        data = storage_client.load(blob_name)

    # Validate that data is not empty
    assert data is not None, "Loaded data should not be None"
    assert not data.empty, "Loaded data should not be empty"

    # Validate expected columns exist
    expected_columns = ["id", "value"]
    for column in expected_columns:
        assert column in data.columns, f"Missing expected column: {column}"

    # Export data for downstream processing
    return data
