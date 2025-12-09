import requests
from typing import Dict
from typing import Any
from bs4 import BeautifulSoup
from typing import List


@transformer
def scrape_article_details(input_data: List[str], *args, **kwargs):
    """
    Fetches each article URL, extracts title, publication date, author, and main content.

    Args:
        input_data (List[str]): List of article URLs.
        **kwargs: Additional arguments if needed.

    Returns:
        List[Dict[str, Any]]: List of dictionaries with article details.
    """

    articles_details: List[Dict[str, Any]] = []

    for url in input_data:
        try:
            # Send HTTP GET request to the article URL
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the title
            title_tag = soup.find("title")
            title = title_tag.get_text(strip=True) if title_tag else ""

            # Extract publication date
            pub_date_tag = (
                soup.find("meta", attrs={"name": "pubdate"})
                or soup.find("meta", attrs={"property": "article:published_time"})
                or soup.find("time")
            )
            pub_date = (
                pub_date_tag["content"]
                if pub_date_tag and "content" in pub_date_tag.attrs
                else ""
            )

            # Extract author
            author_tag = (
                soup.find("meta", attrs={"name": "author"})
                or soup.find("meta", attrs={"property": "article:author"})
                or soup.find("span", class_="author")
            )
            author = (
                author_tag["content"].strip()
                if author_tag and "content" in author_tag.attrs
                else ""
            )

            # Extract main content
            # This is heuristic; may need adjustment based on site structure
            article_body = ""
            article_tags = soup.find_all(
                ["p", "div"], class_=lambda x: x and "content" in x.lower()
            )
            if article_tags:
                article_body = " ".join(
                    tag.get_text(strip=True) for tag in article_tags
                )
            else:
                # fallback: get all paragraph texts
                paragraphs = soup.find_all("p")
                article_body = " ".join(p.get_text(strip=True) for p in paragraphs)

            # Append the extracted details
            articles_details.append(
                {
                    "url": url,
                    "title": title,
                    "publication_date": pub_date,
                    "author": author,
                    "content": article_body,
                }
            )

        except requests.RequestException as e:
            # Handle request errors, optionally log or skip
            articles_details.append(
                {
                    "url": url,
                    "error": str(e),
                }
            )

    return articles_details
