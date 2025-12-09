import pandas as pd


@transformer
def transform_weather_data(input_data: pd.DataFrame, *args, **kwargs):
    """
    Transforms raw weather data by converting temperature from Celsius to Fahrenheit,
    normalizing humidity to percentage, and parsing timestamps into datetime objects.

    Args:
        input_data (pd.DataFrame): DataFrame with columns 'timestamp', 'temperature', 'humidity'.

    Returns:
        pd.DataFrame: Transformed DataFrame with columns 'timestamp', 'temperature_f', 'humidity_percent'.
    """

    # Convert temperature from Celsius to Fahrenheit
    input_data["temperature_f"] = input_data["temperature"] * 9 / 5 + 32

    # Normalize humidity to percentage (assuming humidity is in 0-1 range)
    input_data["humidity_percent"] = input_data["humidity"] * 100

    # Parse timestamps into datetime objects
    input_data["timestamp"] = pd.to_datetime(input_data["timestamp"])

    # Select only the desired columns for output
    output_df = input_data[["timestamp", "temperature_f", "humidity_percent"]]

    return output_df
