import os
import yaml
from typing import Dict, Any


@custom
def update_mage_sources_yaml(source_definitions: Dict[str, Any], *args, **kwargs):
    """
    Reads the existing mage_sources.yml file, merges the provided source definitions,
    and writes back the updated content to ensure source definitions are current.
    This maintains consistency and reflects the latest pipeline dependencies and external data sources.

    Args:
        source_definitions (Dict[str, Any]): The new or updated source definitions to merge.
        yaml_file_path (str): Path to the mage_sources.yml file. Defaults to 'mage_sources.yml'.
    """

    # Load existing YAML content if the file exists
    yaml_file_path: str = "mage_sources.yml"
    if os.path.exists(yaml_file_path):
        with open(yaml_file_path, "r") as file:
            try:
                existing_sources = yaml.safe_load(file) or {}
            except yaml.YAMLError:
                existing_sources = {}
    else:
        existing_sources = {}

    # Merge new source definitions into existing ones
    # This will add new sources, update existing ones, and leave others untouched
    for source_name, source_config in source_definitions.items():
        existing_sources[source_name] = source_config

    # Write the merged sources back to the YAML file atomically
    with open(yaml_file_path, "w") as file:
        yaml.safe_dump(existing_sources, file, default_flow_style=False)
