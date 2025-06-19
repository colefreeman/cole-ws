import re
import pandas as pd
import logging
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from datetime import datetime
import dateutil.parser


@transformer
def clean_and_structure_regulations(data: List[Dict[str, Any]], **kwargs) -> pd.DataFrame:
    """
    Cleans and structures the scraped architecture compliance regulations data.
    
    Args:
         List of dictionaries containing raw scraped regulation data
        
    Returns:
        pd.DataFrame: A structured DataFrame with cleaned regulation data
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f"Starting to clean and structure {len(data)} regulation records")
    
    # Create empty lists to store cleaned data
    cleaned_data = []
    
    # Define architecture categories for classification
    architecture_categories = [
        'residential', 'commercial', 'industrial', 'healthcare', 'educational',
        'accessibility', 'energy efficiency', 'structural', 'fire safety',
        'plumbing', 'electrical', 'mechanical', 'green building', 'historic preservation'
    ]
    
    # Process each regulation record
    for record in 
        try:
            # Clean title - remove any HTML tags if present
            title = record.get('title', '')
            if title:
                if isinstance(title, str):
                    # Remove HTML tags if present
                    soup = BeautifulSoup(title, 'html.parser')
                    title = soup.get_text().strip()
            
            # Clean description - remove any HTML tags if present
            description = record.get('description', '')
            if description:
                if isinstance(description, str):
                    # Remove HTML tags if present
                    soup = BeautifulSoup(description, 'html.parser')
                    description = soup.get_text().strip()
            
            # Standardize date format
            publication_date = record.get('publication_date')
            standardized_date = None
            
            if publication_date:
                try:
                    # Try to parse the date string
                    parsed_date = dateutil.parser.parse(publication_date, fuzzy=True)
                    standardized_date = parsed_date.strftime('%Y-%m-%d')
                except (ValueError, TypeError):
                    # Try to extract date using regex patterns
                    date_patterns = [
                        r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})',  # MM/DD/YYYY or DD/MM/YYYY
                        r'(\w+\s\d{1,2},\s\d{4})',  # Month DD, YYYY
                        r'(\d{4}-\d{2}-\d{2})'  # YYYY-MM-DD
                    ]
                    
                    for pattern in date_patterns:
                        match = re.search(pattern, publication_date)
                        if match:
                            try:
                                date_str = match.group(0)
                                parsed_date = dateutil.parser.parse(date_str, fuzzy=True)
                                standardized_date = parsed_date.strftime('%Y-%m-%d')
                                break
                            except (ValueError, TypeError):
                                continue
            
            # Extract compliance deadline if available in the description
            compliance_deadline = None
            deadline_patterns = [
                r'deadline[:\s]+(\w+\s\d{1,2},\s\d{4})',
                r'due\s+by[:\s]+(\w+\s\d{1,2},\s\d{4})',
                r'compliance\s+date[:\s]+(\w+\s\d{1,2},\s\d{4})',
                r'effective\s+date[:\s]+(\w+\s\d{1,2},\s\d{4})'
            ]
            
            for pattern in deadline_patterns:
                match = re.search(pattern, description, re.IGNORECASE)
                if match:
                    try:
                        deadline_str = match.group(1)
                        parsed_deadline = dateutil.parser.parse(deadline_str, fuzzy=True)
                        compliance_deadline = parsed_deadline.strftime('%Y-%m-%d')
                        break
                    except (ValueError, TypeError, IndexError):
                        continue
            
            # Determine relevant architecture categories based on keywords in title and description
            relevant_categories = []
            combined_text = f"{title} {description}".lower()
            
            for category in architecture_categories:
                if category.lower() in combined_text or category.replace(' ', '-').lower() in combined_text:
                    relevant_categories.append(category)
            
            # Create cleaned record
            cleaned_record = {
                'title': title,
                'description': description,
                'publication_date': standardized_date,
                'compliance_deadline': compliance_deadline,
                'source_url': record.get('link'),
                'source_website': record.get('source'),
                'architecture_categories': ', '.join(relevant_categories) if relevant_categories else 'General',
                'scraped_at': record.get('scraped_at', datetime.now().isoformat())
            }
            
            cleaned_data.append(cleaned_record)
            
        except Exception as e:
            logging.error(f"Error processing record: {str(e)}")
            # Continue with next record instead of failing completely
    
    # Convert to DataFrame
    df = pd.DataFrame(cleaned_data)
    
    # Additional DataFrame cleaning operations
    if not df.empty:
        # Fill missing values
        df['title'] = df['title'].fillna('Untitled Regulation')
        df['description'] = df['description'].fillna('No description available')
        df['architecture_categories'] = df['architecture_categories'].fillna('General')
        
        # Remove duplicate records based on title and publication date
        df = df.drop_duplicates(subset=['title', 'publication_date'], keep='first')
    
    logging.info(f"Successfully cleaned and structured {len(df)} regulation records")
    return df