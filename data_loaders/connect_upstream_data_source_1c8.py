import os
from typing import Dict, Any
import yaml


@data_loader
def main(*args, **kwargs):
    """
    Connects upstream Mage blocks (Python, SQL, R) to downstream dbt models by
    generating or updating the mage_sources.yml file based on upstream block metadata.
    """

    # Retrieve upstream block metadata from kwargs
    upstream_blocks: Dict[str, Any] = kwargs.get("upstream_blocks", {})

    # Initialize the sources list
    sources = []

    # Loop through upstream blocks to extract relevant info
    for block_uuid, block_info in upstream_blocks.items():
        # Only process if block is a data loader (Python, SQL, R)
        block_type = block_info.get("type")
        if block_type not in ("data_loader", "transformer", "custom"):
            continue

        # Extract block name and pipeline info
        block_name = block_info.get("name", f"block_{block_uuid}")
        pipeline_uuid = block_info.get("pipeline_uuid", "unknown_pipeline")

        # Generate source table name and identifier
        source_name = f"mage_{pipeline_uuid}"
        table_name = f"{pipeline_uuid}_{block_uuid}"

        # Build source dict
        source_entry = {
            "description": f"Dataframe for block `{block_name}` of the `{pipeline_uuid}` Mage pipeline.",
            "loader": "mage",
            "name": source_name,
            "schema": "public",
            "tables": [
                {
                    "description": f"Dataframe for block `{block_name}` of the `{pipeline_uuid}` Mage pipeline.",
                    "identifier": table_name,
                    "meta": {
                        "block_uuid": block_uuid,
                        "pipeline_uuid": pipeline_uuid,
                    },
                    "name": table_name,
                }
            ],
        }

        sources.append(source_entry)

    # Compose the full mage_sources.yml content
    yaml_content = {
        "version": 2,
        "sources": sources,
    }

    # Convert to YAML string

    yaml_str = yaml.dump(yaml_content, sort_keys=False)

    # Write to mage_sources.yml in the current directory
    yaml_path = os.path.join(os.getcwd(), "mage_sources.yml")
    with open(yaml_path, "w") as yaml_file:
        yaml_file.write(yaml_str)

    # Optional: print confirmation
    print(f"Generated mage_sources.yml with {len(sources)} sources at {yaml_path}")


@test
def test_generate_mage_sources(
    output_data_from_main,
):
    """
    Test to verify mage_sources.yml is generated correctly with expected content.
    """
    yaml_path = os.path.join(os.getcwd(), "mage_sources.yml")
    assert os.path.exists(yaml_path), "mage_sources.yml file was not created."

    with open(yaml_path, "r") as f:
        content = yaml.safe_load(f)

    assert "version" in content and content["version"] == 2, "Incorrect YAML version."
    assert "sources" in content, "Sources key missing in YAML."
    assert isinstance(content["sources"], list), "Sources should be a list."
    # Further checks can be added based on upstream_blocks mock data
