from deltalake.writer import write_deltalake
if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(df, *args, **kwargs):
    """
    Export data to a Delta Table

    Docs: https://delta-io.github.io/delta-rs/python/usage.html#writing-delta-tables
    """
    storage_options = {
        'AWS_ACCESS_KEY_ID': '',
        'AWS_SECRET_ACCESS_KEY': '',
        'AWS_REGION': '',
        'AWS_S3_ALLOW_UNSAFE_RENAME': 'true',
    }

    uri = 's3://[bucket]/[key]'

    write_deltalake(
        uri,
        data=df,
        mode='append',          # append or overwrite
        overwrite_schema=False, # set True to alter the schema when overwriting
        partition_by=[],
        storage_options=storage_options,
    )
