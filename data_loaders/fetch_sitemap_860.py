import xml.etree.ElementTree as ET
import requests
from typing import List


@data_loader
def fetch_sitemap(*args, **kwargs):
    """
    Fetches the sitemap XML from AuntMinnie.com, parses it,
    and returns a list of URLs for subsequent processing.
    """

    # URL of the sitemap XML
    sitemap_url: str = "https://www.auntminnie.com/sitemap.xml"

    # Send HTTP GET request to fetch the sitemap XML
    response: requests.Response = requests.get(sitemap_url)

    # Raise an exception if the request was unsuccessful
    response.raise_for_status()

    # Parse the XML content
    root: ET.Element = ET.fromstring(response.content)

    # Initialize list to hold URLs
    urls: List[str] = []

    # Iterate over each <loc> element in the sitemap
    for loc in root.findall(".//loc"):
        if loc.text:
            urls.append(loc.text)

    return urls
