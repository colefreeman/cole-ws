from requests.exceptions import RequestException
import requests
from requests.exceptions import HTTPError


@data_loader
def fetch_api_data(*args, **kwargs):
    """
    Fetch data from a public API endpoint using a GET request.

    Args:
        url (str): The API endpoint URL.
        **kwargs: Additional arguments to pass to requests.get().

    Returns:
        Optional[Dict[str, Any]]: The JSON response data if successful, None otherwise.
    """

    url: str = None
    try:
        # Send GET request to the specified URL with optional parameters
        response = requests.get(url, **kwargs)
        # Raise an exception for HTTP error responses
        response.raise_for_status()
        # Parse and return JSON data
        data = response.json()
        return data
    except HTTPError as http_err:
        # Handle HTTP errors
        print(f"HTTP error occurred: {http_err}")
    except RequestException as req_err:
        # Handle other request-related errors
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        # Handle JSON decoding errors
        print(f"JSON decode error: {json_err}")
    except Exception as err:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {err}")

    return None
