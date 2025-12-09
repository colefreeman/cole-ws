import pandas as pd


@transformer
def process_data(data: pd.DataFrame, *args, **kwargs):
    """
    Cleanses and processes input DataFrame from upstream block.

    Args:
        data (pd.DataFrame): Input DataFrame from upstream block 'connect_upstream_data_source_dcd'.
        **kwargs: Additional keyword arguments.

    Returns:
        pd.DataFrame: Processed DataFrame with cleansed and aggregated data.
    """

    # Check if input data is empty
    if data is None or data.empty:
        # Return empty DataFrame with expected schema
        return pd.DataFrame(columns=["id", "value", "category", "timestamp"])

    # Handle missing or malformed data
    # Drop rows with missing 'id' or 'value'
    data = data.dropna(subset=["id", "value"])

    # Convert 'id' to string
    data["id"] = data["id"].astype(str)

    # Convert 'value' to float, handle errors
    data["value"] = pd.to_numeric(data["value"], errors="coerce")

    # Drop rows where 'value' could not be converted
    data = data.dropna(subset=["value"])

    # Convert 'timestamp' to datetime, handle errors
    if "timestamp" in data.columns:
        data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
        # Drop rows with invalid timestamps
        data = data.dropna(subset=["timestamp"])
    else:
        # If 'timestamp' not present, create a default timestamp
        data["timestamp"] = pd.Timestamp.now()

    # Apply business rule: filter out entries with 'value' less than zero
    data = data[data["value"] >= 0]

    # Aggregate data: compute sum of 'value' per 'category'
    if "category" in data.columns:
        aggregated_data = data.groupby("category", as_index=False).agg({"value": "sum"})
        # Add a 'timestamp' column with current timestamp
        aggregated_data["timestamp"] = pd.Timestamp.now()
        # Rename columns for clarity
        processed_df = aggregated_data.rename(
            columns={"category": "category", "value": "total_value"}
        )
    else:
        # If 'category' not present, aggregate overall sum
        total_value = data["value"].sum()
        processed_df = pd.DataFrame(
            {
                "category": ["all"],
                "total_value": [total_value],
                "timestamp": [pd.Timestamp.now()],
            }
        )

    # Return the processed DataFrame
    return processed_df
