from typing import Any, Dict, Optional

from httpx import AsyncClient

from backend.core.logger import logger
from backend.areas.config import all_areas
from backend.areas.finder import area_finder, find_nearest_feature
from backend.exceptions import AreaNotFound, AreaNotSupported


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
        area_teryt = area_finder.area_at(lat, lon)
        if area_teryt not in all_areas:
            raise AreaNotSupported(area_teryt)

    except AreaNotFound:
        logger.warning(f'Error finding area at {lat} {lon}')
        return data
    except AreaNotSupported as msg:
        logger.exception(msg)
        return data

    area = all_areas[area_teryt]
    url = area.build_url(lat, lon)
    logger.info(f'Downloading data for {area_teryt} from: {url}')
    async with AsyncClient(verify=False) as client:
        try:
            gml_content = await _download_gml(client, url)
            if not gml_content:
                return data

            logger.debug(gml_content)
            geojson = area.parse_gml_to_geojson(gml_content)

            if len(geojson['features']) > 1:
                geojson['features'] = [find_nearest_feature(lat, lon, geojson)]

            area.replace_properties_with_osm_tags(geojson)
            data = geojson
        except IOError as e:
            logger.warning(f'Error on downloading building from: {url} {e}')
        except ValueError as e:
            logger.warning(f'Error on parsing response: {data} {e}')

    return data
