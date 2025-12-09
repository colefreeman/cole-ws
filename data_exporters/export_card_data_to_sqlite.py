import os
from typing import Any

import pandas as pd
import sqlite3
from mage_ai.settings.repo import get_repo_path


@data_exporter
def save_df_to_sqlite(df: pd.DataFrame, **kwargs: Any) -> None:
    """
    Save a pandas DataFrame to a SQLite database.

    Args:
        **kwargs: Arguments including:
            df: Input pandas DataFrame to save 
            table: Name of the table to create/write to in SQLite (default: "default_table")
            database: Path to SQLite database file (default: "database.db")
            Additional arguments to pass to pandas to_sql() function
    
    Returns:
        None
    """
    table = kwargs.get('table', 'magic_cards') 
    database = os.path.join(get_repo_path(), kwargs.get('database', 'examples.db'))

    df = clean_dataframe_for_json(df)
    
    with sqlite3.connect(database) as conn:
        df.to_sql(name=table, con=conn, if_exists='replace', index=False)

    return df



def clean_dataframe_for_json(df):
    """Clean DataFrame by handling problematic UTF-8 characters"""
    def clean_value(value):
        if isinstance(value, str):
            try:
                # Attempt to encode/decode to clean the string
                return value.encode('utf-8', errors='replace').decode('utf-8')
            except:
                return str(value.encode('ascii', errors='replace').decode('ascii'))
        return value

    # Apply cleaning to all string columns
    for column in df.select_dtypes(include=['object']).columns:
        df[column] = df[column].apply(clean_value)
    
    return df