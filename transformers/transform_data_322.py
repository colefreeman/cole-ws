import pandas as pd


@transformer
def transform_data_322(
    data: object,
    **kwargs,
) -> object:
    """
    Transforms the input data by performing data quality checks,
    cleaning, and applying necessary transformations to prepare
    for export.
    """

    # Check if data is None or empty
    if data is None:
        raise ValueError("Input data is None.")
    if not hasattr(data, "__len__") or len(data) == 0:
        raise ValueError("Input data is empty.")

    # Import pandas locally to avoid import at top-level (per best practices in blocks)

    if not isinstance(data, pd.DataFrame):
        df = pd.DataFrame(data)
    else:
        df = data.copy()

    # Data quality checks: drop duplicates
    df.drop_duplicates(inplace=True)

    # Handle missing values: fill with default or drop
    # For example, fill missing with empty string or zero
    for column in df.columns:
        if df[column].dtype == "object":
            df[column].fillna("", inplace=True)
        elif pd.api.types.is_numeric_dtype(df[column]):
            df[column].fillna(0, inplace=True)
        else:
            df[column].fillna("", inplace=True)

    # Example transformation: create a new column based on existing data
    # For illustration, suppose we create a 'status' column
    if "status" not in df.columns:
        df["status"] = "active"

    # Additional transformations can be added here
    # e.g., normalize data, encode categorical variables, etc.

    # Return the transformed DataFrame
    return df
