from typing import Any, Dict, Optional

from httpx import AsyncClient

from backend.core.logger import logger
from backend.counties.config import all_counties
from backend.counties.egib_to_osm import egib_to_osm
from backend.counties.finder import county_finder
from backend.counties.parsers.utils import gml_to_geojson
from backend.exceptions import CountyNotFound, CountyNotSupported


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


async def get_building_at(lat: float, lon: float) -> Dict[str, Any]:
    data = {'type': 'FeatureCollection', 'features': []}
    try:
        county_teryt = county_finder.county_at(lat, lon)
        if county_teryt not in all_counties:
            raise CountyNotSupported(county_teryt)

    except CountyNotFound:
        logger.warning(f'Error finding county at {lat} {lon}')
        return data
    except CountyNotSupported as msg:
        logger.exception(msg)
        return data

    url = all_counties[county_teryt].build_url(lat, lon)
    async with AsyncClient() as client:
        try:
            gml_content = await _download_gml(client, url)
            if not gml_content:
                return data
            logger.debug(gml_content)
            geojson = gml_to_geojson(gml_content)

            # Avoid multiple buildings (it shouldn't normally occur)
            # order/distance doesn't matter
            if len(geojson['features']) > 1:
                geojson['features'] = [geojson['features'][0]]

            egib_to_osm(geojson, county_teryt)
            data = geojson
        except IOError as e:
            logger.warning(f'Error on downloading building from: {url} {e}')
        except ValueError as e:
            logger.warning(f'Error on parsing response: {data} {e}')

    return data
