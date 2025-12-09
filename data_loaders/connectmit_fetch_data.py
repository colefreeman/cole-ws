import pandas as pd
import requests

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def load_data_from_github(*args, **kwargs):
    """
    Load data from GitHub and convert to DataFrame
    """
    url = "https://raw.githubusercontent.com/mage-ai/datasets/master/french_sales_data.json"
    
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data['sales_transactions'])
    
    return df