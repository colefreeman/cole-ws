import io
import random

import polars as pl
import requests

@data_loader
def load_data_from_api(*args, **kwargs):
    url = 'https://raw.githubusercontent.com/mage-ai/datasets/refs/heads/master/medical_hospital.csv'
    response = requests.get(url)

    data = pl.read_csv(io.StringIO(response.text))

    # Initial chunk size
    chunk_size = 100
    total_rows = len(data)
    current_pos = 0
    chunk_count = 0
    
    print(f'Total rows loaded: {total_rows}')

    while current_pos < total_rows:
        chunk_count += 1
        # Get chunk with current size
        chunk = data[current_pos:current_pos + chunk_size]
        
        print(f'Yielding chunk {chunk_count}: Rows {current_pos} to {current_pos + len(chunk)}')
        print(f'Chunk size: {chunk_size}')
        
        # Increment chunk size and position
        chunk_size += (50 * random.randint(1, chunk_count))
        current_pos += len(chunk)

        yield chunk