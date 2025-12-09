from typing import List
import requests
from bs4 import BeautifulSoup


@transformer
def parse_article_urls(sitemap_urls: List[str], *args, **kwargs):
    """
    Parses a list of sitemap URLs to extract article links related to radiology news articles.

    Args:
        sitemap_urls (List[str]): List of URLs from the sitemap to process.

    Returns:
        List[str]: List of article URLs extracted from the pages.
    """

    article_links: List[str] = []

    for url in sitemap_urls:
        try:
            # Send GET request to fetch the page content
            response = requests.get(url)
            response.raise_for_status()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all anchor tags that link to articles
            # Assuming articles are linked with <a> tags containing 'radiology' or similar keywords
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                # Filter URLs that are related to radiology news articles
                if "radiology" in href.lower() and href.startswith("http"):
                    article_links.append(href)
                elif "radiology" in href.lower() and not href.startswith("http"):
                    # Handle relative URLs
                    base_url = requests.utils.urlparse(url)
                    full_url = requests.compat.urljoin(base_url.geturl(), href)
                    article_links.append(full_url)
        except requests.RequestException:
            # Log or handle request errors if needed
            continue

    # Remove duplicates
    unique_article_links = list(set(article_links))
    return unique_article_links
