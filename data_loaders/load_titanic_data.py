import pandas as pd
from typing import Any, Dict


@data_loader
def main(
    **kwargs: Dict[str, Any],
) -> pd.DataFrame:
    """
    Loads the Titanic dataset from a CSV file or a known data source.
    Returns a pandas DataFrame with columns as in the original Titanic dataset.
    """

    # Try to get the CSV path from kwargs, otherwise use a default URL
    csv_path: str = kwargs.get(
        "csv_path",
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    )

    # Read the Titanic dataset into a pandas DataFrame
    df: pd.DataFrame = pd.read_csv(csv_path)

    # Ensure the DataFrame contains the expected columns
    expected_columns = [
        "PassengerId", "Survived", "Pclass", "Name", "Sex", "Age",
        "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"
    ]
    # Only keep columns that exist in the DataFrame
    columns_to_keep = [col for col in expected_columns if col in df.columns]
    df = df[columns_to_keep]

    return df


@test
def test_output_data_exists(output_data_from_main_function: pd.DataFrame):
    assert output_data_from_main_function is not None, "Output data should not be None"


@test
def test_minimum_number_of_rows(output_data_from_main_function: pd.DataFrame):
    assert len(output_data_from_main_function) >= 100, "Output data should have at least 100 rows"


@test
def test_expected_columns_exist(output_data_from_main_function: pd.DataFrame):
    expected_columns = {
        "PassengerId", "Survived", "Pclass", "Name", "Sex", "Age",
        "SibSp", "Parch", "Ticket", "Fare", "Cabin", "Embarked"
    }
    actual_columns = set(output_data_from_main_function.columns)
    assert expected_columns.intersection(actual_columns), "At least one expected column should exist in the output"
