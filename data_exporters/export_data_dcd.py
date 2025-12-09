import os
from typing import Any, Dict, List
import psycopg2


@data_exporter
def main(input_data: List[Dict[str, Any]], *args, **kwargs):
    """
    Export processed data to a target data warehouse or storage system.
    Connects to the target system, authenticates, and loads data efficiently.
    """

    # Retrieve secrets for authentication
    db_user = get_secret_value(
        "POSTGRES_PWD"
    )  # Assuming PostgreSQL; adjust key as needed
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("DB_PORT", "5432")
    db_name = os.environ.get("DB_NAME", "my_database")

    # Establish database connection
    try:
        connection = psycopg2.connect(
            user=db_user,
            host=db_host,
            port=db_port,
            dbname=db_name,
        )
        cursor = connection.cursor()
    except Exception as e:
        raise RuntimeError(f"Failed to connect to database: {e}")

    # Define target table
    target_table = "exported_data"

    # Prepare insert statement based on input data schema
    if not input_data:
        return

    columns = input_data[0].keys()
    columns_list = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    insert_query = (
        f"INSERT INTO {target_table} ({columns_list}) VALUES ({placeholders})"
    )

    # Batch insert data for efficiency
    batch_size = 1000
    batch = []

    for record in input_data:
        values = [record.get(col) for col in columns]
        batch.append(values)

        if len(batch) >= batch_size:
            try:
                cursor.executemany(insert_query, batch)
                connection.commit()
            except Exception as e:
                connection.rollback()
                raise RuntimeError(f"Failed to insert batch: {e}")
            batch.clear()

    # Insert remaining records
    if batch:
        try:
            cursor.executemany(insert_query, batch)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise RuntimeError(f"Failed to insert final batch: {e}")

    # Close connection
    cursor.close()
    connection.close()
