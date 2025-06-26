import time

import polars as pl


@data_exporter
def export_data(df: pl.DataFrame, *args, **kwargs):
    df = df.with_columns([
        ((pl.col('age') / 10).floor() * 10).alias('age_range')
    ])
    return df