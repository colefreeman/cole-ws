import requests
import pandas as pd
from data_loader import get_secret_value


@data_loader
def fetch_weather_data(*args, **kwargs):
    """
    Fetches current weather data from a public weather API (OpenWeatherMap).
    Returns:
        pd.DataFrame: DataFrame containing weather parameters such as temperature,
                      humidity, wind speed, and location details.
    """

    # API endpoint for current weather data (replace 'YOUR_API_KEY' with your actual API key)
    api_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "New York,US",  # Location query; modify as needed
        "appid": get_secret_value(
            "OPENWEATHERMAP_API_KEY"
        ),  # Fetch API key from secrets
        "units": "metric",  # Use 'imperial' for Fahrenheit
    }

    # Send GET request to the weather API
    response = requests.get(api_url, params=params)
    response.raise_for_status()

    # Parse JSON response
    data = response.json()

    # Extract relevant weather parameters
    weather_data = {
        "location": data.get("name"),
        "latitude": data["coord"].get("lat"),
        "longitude": data["coord"].get("lon"),
        "temperature_c": data["main"].get("temp"),
        "humidity": data["main"].get("humidity"),
        "wind_speed_m_s": data["wind"].get("speed"),
        "weather_description": data["weather"][0].get("description"),
        "timestamp": pd.to_datetime(data.get("dt"), unit="s"),
    }

    # Convert to DataFrame
    df = pd.DataFrame([weather_data])

    return df
