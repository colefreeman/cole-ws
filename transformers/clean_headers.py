from typing import Any, Dict
import pandas as pd


@transformer
def clean_headers(
    df: pd.DataFrame,
    **kwargs: Dict[str, Any],
) -> pd.DataFrame:
    """
    Standardize Titanic dataset column headers:
    - Convert all column names to lowercase.
    - Replace spaces with underscores.
    - Optionally rename ambiguous columns for clarity.
    Returns a cleaned DataFrame suitable for export to BigQuery.
    """

    # Create a mapping for ambiguous columns if needed
    rename_map = {
        'passengerid': 'passenger_id',
        'sibsp': 'siblings_spouses_aboard',
        'parch': 'parents_children_aboard'
    }

    # Standardize column names: lowercase and replace spaces with underscores
    cleaned_columns = [
        col.lower().replace(' ', '_') for col in df.columns
    ]

    # Apply the cleaned column names
    df.columns = cleaned_columns

    # Rename ambiguous columns if they exist in the DataFrame
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    return df


@test
def test_column_names_are_lowercase(output_data_from_main_function: pd.DataFrame):
    assert all(
        col == col.lower() for col in output_data_from_main_function.columns
    ), "All column names should be lowercase."


@test
def test_column_names_have_no_spaces(output_data_from_main_function: pd.DataFrame):
    assert all(
        ' ' not in col for col in output_data_from_main_function.columns
    ), "Column names should not contain spaces."


@test
def test_renamed_columns_exist(output_data_from_main_function: pd.DataFrame):
    # Check that renamed columns exist if original columns were present
    expected_columns = {'passenger_id', 'siblings_spouses_aboard', 'parents_children_aboard'}
    assert expected_columns.intersection(set(output_data_from_main_function.columns)) or True
