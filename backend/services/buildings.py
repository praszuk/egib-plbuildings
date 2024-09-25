from tarfile import StreamError
from typing import Any, Dict, Optional

from fastapi import HTTPException
from httpx import AsyncClient, TimeoutException, NetworkError

from backend.core.logger import default_logger
from backend.areas.config import all_areas
from backend.areas.finder import area_finder, find_nearest_feature
from backend.exceptions import AreaNotFound, ParserError


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
    try:
        area_teryt = area_finder.area_at(lat, lon)
        if area_teryt not in all_areas:
            default_logger.warning(
                f'Area not supported ({area_teryt})',
                extra={
                    'area_teryt': area_teryt,
                },
            )
            raise HTTPException(
                status_code=501, headers={'X-Error': f'Area not supported ({area_teryt})'}
            )

    except AreaNotFound:
        default_logger.warning(f'Area not found at {lat} {lon}')
        raise HTTPException(status_code=404, headers={'X-Error': f'Area not found at {lat} {lon}'})

    area = all_areas[area_teryt]
    url = area.build_buildings_bbox_url(lat, lon)
    default_logger.info(
        f'Downloading data for {area_teryt} from: {url}',
        extra={
            'area_teryt': area_teryt,
            'area_name': area.name,
            'lat': lat,
            'lon': lon,
            'url': url,
        },
    )
    async with AsyncClient(verify=False) as client:
        try:
            gml_content = await _download_gml(client, url)
            if not gml_content:
                raise HTTPException(
                    status_code=502, headers={'X-Error': 'Incorrect data from external server'}
                )

            default_logger.debug(gml_content)
            geojson = area.parse_gml_to_geojson(gml_content)

            if len(geojson['features']) > 1:
                geojson['features'] = [find_nearest_feature(lat, lon, geojson)]

            area.replace_properties_with_osm_tags(geojson)

            return geojson
        except (TimeoutException, NetworkError, StreamError):
            raise HTTPException(status_code=503, headers={'X-Error': 'Server not respond'})
        except ParserError as e:
            default_logger.warning(f'Error on parsing response: {e}')
            raise HTTPException(
                status_code=502, headers={'X-Error': 'Error at parsing data from server'}
            )
