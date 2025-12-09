from typing import Any, Dict, List

import pandas as pd
import requests


@data_loader
def get_mtg_cards(**kwargs: Any) -> pd.DataFrame:
    """
    Fetches Magic The Gathering card data from API and returns as Pandas DataFrame

    Args:
    **kwargs: Arbitrary keyword arguments

    Returns:
    pd.DataFrame: Pandas DataFrame containing card data
    """
    api_url = "https://api.magicthegathering.io/v1/cards?pageSize=10"
    response = requests.get(api_url)
    response.raise_for_status()

    cards_data: List[Dict[str, Any]] = response.json()["cards"]

    return pd.DataFrame(cards_data)

