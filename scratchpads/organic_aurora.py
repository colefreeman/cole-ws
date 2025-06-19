"""
NOTE: Scratchpad blocks are used only for experimentation and testing out code.
The code written here will not be executed as part of the pipeline.
"""
from data_integrations.sources.spacex_api import SpaceXAPI

# Replace with your actual config keys and values
config = dict(
)

# Initialize the source class with config
source = SpaceXAPI(config=config)

# Run stream discovery
streams = source.discover_streams()

# Print discovered streams
print(f'Discovered streams: {streams}')