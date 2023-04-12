import logging
from typing import Any, Dict, Optional, Tuple

from httpx import AsyncClient

from backend.exceptions import PowiatNotFound
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


def _get_powiat_url(
    powiat_teryt: str, bbox: Tuple[float, float, float, float]
) -> str:
    """
    Creates URL string to download building data for give powiat area.

    :param powiat_teryt: 4 digit as string1
    :param bbox: lat, lon, lat, lon comma EPSG:4326 (WSG84)
    :raises: PowiatNotFound
    :return: build URL string to download data
    """
    if powiat_teryt == '1421':
        return (
            'https://wms.epodgik.pl/cgi-bin/pruszkow/wfs'
            '?service=wfs'
            '&version=2.0.0'
            '&request=GetFeature'
            '&typeNames=ms:budynki'
            f'&SRSNAME={_SRSNAME}'
            f'&bbox={",".join(map(str, bbox))},{_SRSNAME}'
        )

    raise PowiatNotFound()


async def get_building_at(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    powiat_teryt = get_powiat_teryt_at(lat, lon)
    try:
        url = _get_powiat_url(powiat_teryt, (lat, lon, lat, lon))
    except PowiatNotFound:
        return None

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
