from typing import Any, Dict

from backend.areas.config import all_areas
from backend.areas.parsers.utils import clean_empty_tags
from backend.exceptions import AreaNotSupported


def egib_to_osm(geojson: Dict[str, Any], teryt: str) -> None:
    """
    Change EGiB properties to OSM tags
    :param geojson: raw EGIB GeoJSON from one wfs service/area
    :param teryt: 4 digit area ("Powiat") number as str
    :raises ParserNotFound, InvalidKeyParserError, ParserError:
    """
    try:
        parser = all_areas[teryt].data_parser
    except KeyError:
        raise AreaNotSupported(teryt)

    for index, feature in enumerate(geojson['features']):
        osm_tags = parser(feature['properties'])
        osm_tags = clean_empty_tags(osm_tags)
        geojson['features'][index]['properties'] = osm_tags
