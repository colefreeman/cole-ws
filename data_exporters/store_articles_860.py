import csv
import os
from typing import List


@data_exporter
def store_articles(articles: list[dict], *args, **kwargs):
    """
    Store a list of article detail dictionaries into a CSV file for further analysis.
    Assumes each dictionary has consistent keys representing article attributes.
    """

    # Define the output CSV file path
    output_dir = os.getenv("DATA_OUTPUT_PATH", "/tmp")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "articles.csv")

    # Check if articles list is empty
    if not articles:
        return

    # Extract headers from the first article dictionary
    headers: List[str] = list(articles[0].keys())

    # Write data to CSV file
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        # Write header row
        writer.writeheader()
        # Write article data rows
        for article in articles:
            # Ensure all keys are present in each article dict
            row = {key: article.get(key, "") for key in headers}
            writer.writerow(row)

    # No return value
