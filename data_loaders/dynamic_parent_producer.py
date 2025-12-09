from typing import Dict, List


@data_loader
def create_list(**kwargs: Dict) -> List[Dict]:
    return [
        [dict(uuid=i) for i in range(3)],
    ]

