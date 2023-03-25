from httpx import AsyncClient

import logging

from typing import Any, Dict, Optional

from utils import gml_to_geojson


_SRSNAME = 'EPSG:4326'


async def get_building_at(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    bbox = f'{lat},{lon},{lat},{lon}'

    url = 'https://wms.epodgik.pl/cgi-bin/pruszkow/wfs' \
          '?service=wfs' \
          '&version=2.0.0' \
          '&request=GetFeature' \
          '&typeNames=ms:budynki' \
          f'&SRSNAME={_SRSNAME}' \
          f'&bbox={bbox},{_SRSNAME}'

    data = {}
    async with AsyncClient() as client:
        try:
            response = await client.get(url)
            geojson = gml_to_geojson(response.text)
            # TODO gugik geojson to osm geojson
            data = geojson  # TODO temporary to test
        except IOError as e:
            logging.warning(f'Error on downloading building from: {url} {e}')
        except ValueError as e:
            logging.warning(f'Error on parsing response: {data} {e}')

    # empty response or unexpected server error
    if 'features' not in data:
        return

    return data
