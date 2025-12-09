import pandas as pd
from typing import Any


@transformer
def transform_data(data: Any, *args, **kwargs):
    """
    Transforms raw API data into a structured DataFrame suitable for BigQuery ingestion.

    Args:
        data: The raw data fetched from the API, type is unknown.
        **kwargs: Additional keyword arguments if needed.

    Returns:
        pd.DataFrame: Transformed data ready for loading into BigQuery.
    """

    # Convert raw data to DataFrame if it's a list of dicts
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        # If data is a dict, attempt to extract relevant part
        # For example, if data contains a key 'results' with list of records
        if "results" in data and isinstance(data["results"], list):
            df = pd.DataFrame(data["results"])
        else:
            # Fallback: create DataFrame from dict keys and values
            df = pd.DataFrame([data])
    else:
        # If data is of unknown type, attempt to convert to DataFrame directly
        df = pd.DataFrame(data)

    # Example: Rename columns to match BigQuery schema
    column_mapping = {
        "id": "record_id",
        "name": "full_name",
        "date": "record_date",
        "value": "measurement_value",
        # Add more mappings as needed
    }
    df.rename(columns=column_mapping, inplace=True)

    # Convert date columns to datetime
    if "record_date" in df.columns:
        df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")

    # Ensure measurement_value is float
    if "measurement_value" in df.columns:
        df["measurement_value"] = pd.to_numeric(
            df["measurement_value"], errors="coerce"
        )

    # Filter out records with missing essential fields
    df.dropna(subset=["record_id", "full_name", "record_date"], inplace=True)

    # Optional: Perform aggregation if needed
    # For example, get average measurement per name per day
    # df = df.groupby(['full_name', 'record_date']).agg({'measurement_value': 'mean'}).reset_index()

    # Additional transformations can be added here as needed

    return df
