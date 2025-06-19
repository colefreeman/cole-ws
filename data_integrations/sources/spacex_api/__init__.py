from mage_integrations.sources.base import Source, main
from mage_integrations.sources.catalog import Catalog
from singer import catalog as catalog_singer
import requests

class SpaceXAPI(Source):
    def test_connection(self):
        response = requests.get("https://api.spacexdata.com/v4/launches/upcoming")
        if response.status_code != 200:
            raise Exception("Connection test failed.")

    def discover(self, streams=None):
        catalog_entries = []
        schema = catalog_singer.Schema.from_dict({
            'properties': {
                'name': {'type': ['string']},
                'date_utc': {'type': ['string'], 'format': 'date-time'},
                'rocket': {'type': ['string']},
                'launchpad': {'type': 'string'},
                'success': {'type': ['boolean', 'null']},
                'details': {'type': ['string', 'null']}
            },
            'type': 'object'
        })
        catalog_entries.append(self.build_catalog_entry(
            'upcoming_launches',
            schema,
        ))
        return Catalog(catalog_entries)

    def load_data(
            self,
            stream,
            *args,
            **kwargs,
        ):
        response = requests.get("https://api.spacexdata.com/v4/launches/upcoming")
        launches = response.json()
        for launch in launches:
            yield [{
                'name': launch.get('name'),
                'date_utc': launch.get('date_utc'),
                'rocket': launch.get('rocket'),
                'launchpad': launch.get('launchpad'),
                'success': launch.get('success'),
                'details': launch.get('details')
            }]

if __name__ == "__main__":
    main(SpaceXAPI)