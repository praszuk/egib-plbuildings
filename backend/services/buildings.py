from httpx import AsyncClient

import logging

from typing import Any, Dict, Optional

from backend.parsers.egib_to_osm import egib_to_osm
from backend.utils import get_powiat_teryt_at, gml_to_geojson


_SRSNAME = 'EPSG:4326'


async def _download_gml(client: AsyncClient, url: str) -> Optional[str]:
    """
    Downloads GML data from URL
    :param client: AsyncClient
    :return: data as string or None
    """
    response = await client.get(url)
    if response.status_code != 200:
        return None

    return response.text


async def get_building_at(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    bbox = f'{lat},{lon},{lat},{lon}'

    powiat_teryt = get_powiat_teryt_at(lat, lon)

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
            gml_content = await _download_gml(client, url)
            if not gml_content:
                return

            geojson = gml_to_geojson(gml_content)

            # Avoid multiple buildings (it shouldn't normally occur)
            # order/distance doesn't matter
            if len(geojson['features']) > 1:
                geojson['features'] = [geojson['features'][0]]

            egib_to_osm(geojson, powiat_teryt)
            data = geojson
        except IOError as e:
            logging.warning(f'Error on downloading building from: {url} {e}')
        except ValueError as e:
            logging.warning(f'Error on parsing response: {data} {e}')

    # empty response or unexpected server error
    if 'features' not in data:
        return

    return data
