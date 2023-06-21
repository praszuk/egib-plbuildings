from typing import Any, Dict

from backend.exceptions import PowiatNotSupported
from backend.powiats.config import all_powiats


def egib_to_osm(geojson: Dict[str, Any], teryt: str) -> None:
    """
    Change EGiB properties to OSM tags
    :param geojson: raw EGIB GeoJSON from one wfs service/powiat
    :param teryt: 4 numbers powiat (county) code as str
    :raises ParserNotFound, InvalidKeyParserError, ParserError:
    """
    try:
        parser = all_powiats[teryt].data_parser
    except KeyError:
        raise PowiatNotSupported(teryt)

    for index, feature in enumerate(geojson['features']):
        osm_tags = parser(feature['properties'])
        geojson['features'][index]['properties'] = osm_tags
