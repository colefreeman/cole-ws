import pandas as pd


@transformer
def transform_weather_data(input_data: pd.DataFrame, *args, **kwargs):
    """
    Cleans and processes raw weather data.

    Args:
        input_data (pd.DataFrame): Raw weather data DataFrame from 'fetch_weather_data_b43'.

    Returns:
        pd.DataFrame: Cleaned and enriched weather data DataFrame.
    """

    # Drop duplicate rows if any
    data = input_data.drop_duplicates()

    # Handle missing values: fill or drop
    # For example, fill missing temperature with mean, drop rows with critical missing data
    if "temperature" in data.columns:
        data["temperature"] = pd.to_numeric(data["temperature"], errors="coerce")
        data["temperature"].fillna(data["temperature"].mean(), inplace=True)

    # Convert timestamp to datetime if not already
    if "timestamp" in data.columns:
        data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")

    # Fill missing values for other columns as needed
    for col in ["humidity", "wind_speed", "precipitation"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
            data[col].fillna(0, inplace=True)

    # Derive weather category based on temperature or other parameters
    if "temperature" in data.columns:
        data["weather_category"] = pd.cut(
            data["temperature"],
            bins=[-50, 0, 15, 25, 35, 50],
            labels=["Freezing", "Cold", "Mild", "Warm", "Hot"],
            include_lowest=True,
        )

    # Format or reformat timestamp if needed
    if "timestamp" in data.columns:
        data["date"] = data["timestamp"].dt.date
        data["hour"] = data["timestamp"].dt.hour

    # Reset index for cleanliness
    data.reset_index(drop=True, inplace=True)

    return data
