import io
import pandas as pd
import requests
from datetime import datetime, timedelta
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from mage_ai.data_preparation.shared.secrets import get_secret_value

@data_loader
def load_data_from_api(**kwargs):
    url='https://data.cityofchicago.org/resource/ijzp-q8t2.csv?$order=updated_on DESC&$limit=10000'
    app_token = get_secret_value('CHICAGO_DATA_API_KEY')
    #year="2023"
    headers = {
        "id": "id",
        "case_number": "case_number",
        "date": "crime_date",
        "block":"block",
        "iucr": "iucr",
        "primary_type": "primary_type",
        "description": "description",
        "location_descrpition": "location_descrpition",
        "arrest": "arrest",
        "domestic": "domestic",
        "beat": "beat",
        "district": "district",
        "ward": "ward",
        "community_area": "community_area",
        "fbi_code": "fbi_code",
        "x_coordinate": "x_coordinate",
        "y_coordinate": "y_coordinate",
        "year": "crime_year",
        "updated_on": "updated_on",
        "latitude": "lat",
        "longitude": "lng",
        "location": "location"
        }
    # Add the year as a query parameter in the API request
    params = {
        '$$app_token': app_token,
        #'year': year
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # Read the CSV data from the response
        raw_crimes_data = pd.read_csv(io.StringIO(response.text), sep=',')

        raw_crimes_data.rename(columns=headers, inplace=True)

        return raw_crimes_data
    else:
        # Handle error cases
        print(f"Failed to retrieve data for year {year}. Status code: {response.status_code}")

    return raw_crimes_data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
