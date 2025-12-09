import os
from typing import Any, Union, Optional

import pandas as pd
import sqlite3
from mage_ai.settings.repo import get_repo_path


@custom
def read_sqlite_table(*args, **kwargs: Any) -> pd.DataFrame:
    """
    Read a SQLite table into a pandas DataFrame.
    
    Args:
        **kwargs: Additional keyword arguments including:
            database (str): SQLite database file path 
            table (str): Name of table to read
            Other arguments passed to pd.read_sql_query()
    
    Returns:
        pd.DataFrame: DataFrame containing the SQLite table data
        None: If there is an error reading the table
    """
    table = kwargs.get('table', 'magic_cards') 
    database = os.path.join(get_repo_path(), kwargs.get('database', 'examples.db'))

    conn = sqlite3.connect(database)
    query = f"SELECT * FROM {table}"
    data = conn.execute(query).fetchall()

    df = pd.DataFrame(data)

    return clean_dataframe_encoding(df)


def clean_dataframe_encoding(df):
    """Clean DataFrame by properly handling binary and encoding issues"""
    def clean_value(value):
        if isinstance(value, bytes):
            # For binary data, convert to hex string
            return value.hex()
        elif isinstance(value, str):
            try:
                # Try to encode as UTF-8 first
                return value.encode('utf-8', errors='replace').decode('utf-8')
            except:
                try:
                    # If that fails, try to decode assuming it's already bytes
                    return value.encode('latin1').decode('utf-8', errors='replace')
                except:
                    # Last resort: force to ASCII
                    return value.encode('ascii', errors='replace').decode('ascii')
        return value

    # Create a copy to avoid modifying original
    df_clean = df.copy()
    
    # Apply cleaning to all object columns
    for column in df_clean.select_dtypes(include=['object']).columns:
        df_clean[column] = df_clean[column].apply(clean_value)
    
    return df_clean