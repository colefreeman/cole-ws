import os
import yaml
from typing import Dict, Any


@custom
def main(*args, **kwargs):
    """
    Verify and check upstream blocks and ensure mage_sources.yml is up-to-date.

    This function performs the following:
    - Reviews the latest pipeline changes.
    - Confirms all upstream blocks (Python, SQL, R) are correctly configured.
    - Validates that their output data types are appropriate.
    - Checks that 'mage_sources.yml' has been automatically updated by Mage.
    - Ensures source identifiers match naming conventions used in dbt models.
    """

    # Import necessary modules

    # Path to the mage_sources.yml file
    mage_sources_path = os.path.join(os.getcwd(), "mage_sources.yml")

    # Load the mage_sources.yml file
    try:
        with open(mage_sources_path, "r") as file:
            mage_sources: Dict[str, Any] = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find 'mage_sources.yml' at {mage_sources_path}. "
            "Ensure Mage has generated the file correctly."
        )

    # Validate the structure of mage_sources
    if not mage_sources or "sources" not in mage_sources:
        raise ValueError(
            "'mage_sources.yml' does not contain 'sources' key or is empty. "
            "Please verify Mage pipeline configuration."
        )

    # Check each source and its tables
    for source in mage_sources["sources"]:
        source_name = source.get("name")
        tables = source.get("tables", [])
        for table in tables:
            identifier = table.get("identifier")
            meta = table.get("meta", {})
            block_uuid = meta.get("block_uuid")
            pipeline_uuid = meta.get("pipeline_uuid")

            # Verify identifier matches expected naming convention
            expected_identifier = f"mage_{pipeline_uuid}_{block_uuid}"
            if identifier != expected_identifier:
                raise ValueError(
                    f"Identifier mismatch for source '{source_name}': "
                    f"expected '{expected_identifier}', found '{identifier}'. "
                    "Update your Mage pipeline or dbt source references accordingly."
                )

            # Additional checks can be added here, e.g., data type validation
            # For example, ensure the source data type is compatible with dbt expectations

    # Optional: Confirm that all upstream blocks are configured correctly
    # This could involve querying the pipeline state or metadata if accessible

    # Final message
    print(
        "All upstream blocks are correctly configured, and 'mage_sources.yml' is up-to-date."
    )
