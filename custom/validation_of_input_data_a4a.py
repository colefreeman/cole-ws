@custom
def main(
    input_data: "DataFrame",
    **kwargs,
) -> "DataFrame":
    """
    Validate that the input DataFrame is not empty and contains expected columns.
    """

    # Assert that the input DataFrame is not empty
    assert not input_data.empty, "Input data should not be empty."

    # Define the expected columns
    expected_columns = ["customer_id", "user_id", "account_type", "status"]

    # Assert that all expected columns are present in the DataFrame
    missing_columns = [col for col in expected_columns if col not in input_data.columns]
    assert not missing_columns, (
        f"Missing expected columns: {', '.join(missing_columns)}"
    )

    # Return the validated DataFrame
    return input_data
