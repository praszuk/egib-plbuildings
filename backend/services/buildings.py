import logging
from typing import Any, Dict, Optional

from httpx import AsyncClient

from backend.exceptions import PowiatNotFound, PowiatNotSupported
from backend.powiats.config import all_powiats
from backend.powiats.egib_to_osm import egib_to_osm
from backend.powiats.finder import powiat_finder
from backend.powiats.parsers.utils import gml_to_geojson


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
    try:
        powiat_teryt = powiat_finder.powiat_at(lat, lon)
        if powiat_teryt not in all_powiats:
            raise PowiatNotSupported(powiat_teryt)

    except PowiatNotFound:
        logging.exception(f'Error finding powiat at {lat} {lon}')
        return None
    except PowiatNotSupported as msg:
        logging.exception(msg)
        return None

    url = all_powiats[powiat_teryt].build_url(lat, lon)
    data = {}
    async with AsyncClient() as client:
        try:
            gml_content = await _download_gml(client, url)
            if not gml_content:
                return None

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
        return None

    return data
