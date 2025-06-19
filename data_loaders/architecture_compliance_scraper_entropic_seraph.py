import requests
import time
import logging
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import re


@data_loader
def scrape_architecture_compliance_regulations(**kwargs) -> pd.DataFrame:
    """
    Scrapes real NYC Building Code content. No fake data.
    
    Returns:
        pd.DataFrame: DataFrame with code_number, code_description, code_exception
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Try different NYC building code URLs
    urls_to_try = [
        'https://www.nyc.gov/site/buildings/codes/2022-construction-codes.page',
        'https://www.nyc.gov/site/buildings/codes/nyc-code.page',
        'https://www.nyc.gov/assets/buildings/apps/pdf_viewer/viewer.html?file=2022BC_Chapter11_AccessibilityWBwm.pdf&section=conscode_2022',
        'https://www.nyc.gov/assets/buildings/apps/pdf_viewer/2022BC_Chapter11_AccessibilityWBwm.pdf',
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    codes_data = []
    
    for url in urls_to_try:
        try:
            logging.info(f"Trying to scrape: {url}")
            time.sleep(2)
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            logging.info(f"Response status: {response.status_code}, Length: {len(response.text)}")
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get all text and log what we find
            all_text = soup.get_text()
            logging.info(f"Text content length: {len(all_text)}")
            logging.info(f"First 1000 chars: {all_text[:1000]}")
            
            # Look for building code patterns
            section_patterns = [
                r'(11\d+(?:\.\d+)*)\s+([^.]+\.)',  # Section number + description
                r'Section\s+(11\d+(?:\.\d+)*)\s+([^.]+\.)',  # "Section 1101.1 Description."
                r'(\d{4}\.\d+(?:\.\d+)*)\s+([^.]+\.)',  # Any 4-digit section
            ]
            
            for pattern in section_patterns:
                matches = re.findall(pattern, all_text, re.IGNORECASE | re.MULTILINE)
                if matches:
                    logging.info(f"Found {len(matches)} matches with pattern: {pattern}")
                    for section_num, description in matches:
                        codes_data.append({
                            'code_number': section_num,
                            'code_description': description.strip(),
                            'code_exception': '',
                            'source_url': url
                        })
            
            # Look for exceptions
            exception_matches = re.findall(r'Exception[:\s]+([^.]+\.)', all_text, re.IGNORECASE)
            logging.info(f"Found {len(exception_matches)} exceptions")
            
            # Look for specific building code terms
            code_terms = ['accessible', 'entrance', 'building', 'shall', 'required']
            for term in code_terms:
                count = all_text.lower().count(term)
                logging.info(f"Found '{term}': {count} times")
            
            # If we found any content, break
            if codes_data:
                logging.info(f"Successfully extracted {len(codes_data)} code sections from {url}")
                break
                
        except Exception as e:
            logging.error(f"Failed to scrape {url}: {str(e)}")
            continue
    
    # Create DataFrame only from real scraped data
    if codes_data:
        df = pd.DataFrame(codes_data)
        logging.info(f"Created DataFrame with {len(df)} real code sections")
        return df
    else:
        logging.warning("No building code data could be extracted from any NYC source")
        return pd.DataFrame(columns=['code_number', 'code_description', 'code_exception'])