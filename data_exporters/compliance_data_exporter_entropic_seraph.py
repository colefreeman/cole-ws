import os
import pandas as pd
import json
import logging
import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional


@data_exporter
def export_compliance_data(df: pd.DataFrame, **kwargs) -> Dict[str, Any]:
    """
    Exports the processed architecture compliance regulations data to various destinations.
    
    This exporter supports multiple export formats:
    - CSV file
    - JSON file
    - SQLite database
    
    Data Schema:
    - title: str - The title of the regulation
    - description: str - Detailed description of the regulation
    - publication_date: str - When the regulation was published (YYYY-MM-DD)
    - compliance_deadline: str - Deadline for compliance (YYYY-MM-DD)
    - source_url: str - URL where the regulation was found
    - source_website: str - Website domain where the regulation was scraped from
    - architecture_categories: str - Comma-separated list of relevant architecture categories
    - scraped_at: str - ISO format timestamp when the data was scraped
    
    In a production environment, this could be connected to:
    - A data warehouse like Snowflake, BigQuery, or Redshift
    - A document database like MongoDB for the full regulation texts
    - An API endpoint for real-time access by other systems
    - A notification system to alert stakeholders about new regulations
    
    Args:
        df: DataFrame containing the processed compliance data
        **kwargs: Additional parameters including export_format and export_path
        
    Returns:
        Dict[str, Any]: Information about the export operation
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Get export parameters from kwargs with defaults
    export_format = kwargs.get('export_format', 'csv').lower()
    export_path = kwargs.get('export_path', './data/compliance_data')
    
    # Add timestamp to filename to avoid overwriting previous exports
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    
    # Add export timestamp to the dataframe
    df['exported_at'] = datetime.now().isoformat()
    
    result = {
        'success': False,
        'format': export_format,
        'timestamp': timestamp,
        'record_count': len(df),
        'path': None,
        'message': None
    }
    
    try:
        if export_format == 'csv':
            # Export to CSV
            file_path = f"{export_path}_{timestamp}.csv"
            df.to_csv(file_path, index=False)
            result['path'] = file_path
            result['success'] = True
            result['message'] = f"Successfully exported {len(df)} records to CSV"
            logging.info(f"Data exported to CSV: {file_path}")
            
        elif export_format == 'json':
            # Export to JSON
            file_path = f"{export_path}_{timestamp}.json"
            
            # Convert DataFrame to JSON with proper formatting
            json_data = df.to_json(orient='records', date_format='iso')
            
            # Write to file with pretty formatting
            with open(file_path, 'w') as f:
                json.dump(json.loads(json_data), f, indent=2)
                
            result['path'] = file_path
            result['success'] = True
            result['message'] = f"Successfully exported {len(df)} records to JSON"
            logging.info(f"Data exported to JSON: {file_path}")
            
        elif export_format == 'sqlite':
            # Export to SQLite database
            db_path = f"{export_path}_{timestamp}.db"
            
            # Create connection to SQLite database
            conn = sqlite3.connect(db_path)
            
            # Write DataFrame to SQLite table
            df.to_sql('architecture_compliance_regulations', conn, if_exists='replace', index=False)
            
            # Create indexes for faster querying
            cursor = conn.cursor()
            cursor.execute('CREATE INDEX idx_publication_date ON architecture_compliance_regulations (publication_date)')
            cursor.execute('CREATE INDEX idx_compliance_deadline ON architecture_compliance_regulations (compliance_deadline)')
            conn.commit()
            conn.close()
            
            result['path'] = db_path
            result['success'] = True
            result['message'] = f"Successfully exported {len(df)} records to SQLite database"
            logging.info(f"Data exported to SQLite database: {db_path}")
            
        else:
            result['message'] = f"Unsupported export format: {export_format}. Supported formats are: csv, json, sqlite"
            logging.error(result['message'])
    
    except Exception as e:
        error_message = f"Error exporting  {str(e)}"
        result['message'] = error_message
        logging.error(error_message)
    
    return result