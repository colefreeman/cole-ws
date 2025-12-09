import requests
from typing import Any
from typing import Dict
import pandas as pd


@data_loader
def fetch_weather_data(*args, **kwargs):
    """
    Fetch weather data from OpenWeatherMap API and return as a pandas DataFrame.

    Args:
        api_url (str): The base URL of the weather API.
        api_key (str): API key for authentication.
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.
        metrics (str): Comma-separated list of weather metrics to retrieve.
        **kwargs: Additional parameters for the API request.

    Returns:
        pd.DataFrame: DataFrame with columns 'timestamp', 'temperature', 'humidity'.
    """

    # Prepare request parameters
    api_url: str = None
    api_key: str = None
    latitude: float = None
    longitude: float = None
    metrics: str = "temperature,humidity"
    params: Dict[str, Any] = {
        "lat": latitude,
        "lon": longitude,
        "appid": api_key,
        "units": "metric",  # Use metric units for temperature
        "exclude": "minutely,daily,alerts",  # Exclude unnecessary data
        **kwargs,
    }

    # Send GET request to the API
    response: requests.Response = requests.get(api_url, params=params)
    response.raise_for_status()

    # Parse JSON response
    data: Dict[str, Any] = response.json()

    # Extract hourly data
    hourly_data: Dict[str, Any] = data.get("hourly", {})

    # Check if hourly data exists
    if not hourly_data:
        return pd.DataFrame(columns=["timestamp", "temperature", "humidity"])

    # Create DataFrame from hourly data
    df: pd.DataFrame = pd.DataFrame(hourly_data)

    # Convert timestamp to datetime
    if "time" in df:
        df["timestamp"] = pd.to_datetime(df["time"])
    else:
        # If 'time' key is missing, fallback to index or other logic
        df["timestamp"] = pd.NaT

    # Select relevant columns
    # Map metrics to their corresponding columns
    metric_mapping: Dict[str, str] = {
        "temperature": "temperature",
        "humidity": "humidity",
    }

    # Initialize output DataFrame
    output_df: pd.DataFrame = pd.DataFrame()

    # Add timestamp column
    output_df["timestamp"] = df["timestamp"]

    # Add temperature column if requested
    if "temperature" in metrics:
        if "temperature" in df:
            output_df["temperature"] = df["temperature"]
        else:
            output_df["temperature"] = pd.NA

    # Add humidity column if requested
    if "humidity" in metrics:
        if "humidity" in df:
            output_df["humidity"] = df["humidity"]
        else:
            output_df["humidity"] = pd.NA

    return output_df
