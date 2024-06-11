from typing import Any, Dict

from backend.counties.config import all_counties
from backend.counties.parsers.utils import clean_empty_tags
from backend.exceptions import CountyNotSupported


def egib_to_osm(geojson: Dict[str, Any], teryt: str) -> None:
    """
    Change EGiB properties to OSM tags
    :param geojson: raw EGIB GeoJSON from one wfs service/county
    :param teryt: 4 digit county ("Powiat") number as str
    :raises ParserNotFound, InvalidKeyParserError, ParserError:
    """
    try:
        parser = all_counties[teryt].data_parser
    except KeyError:
        raise CountyNotSupported(teryt)

    for index, feature in enumerate(geojson['features']):
        osm_tags = parser(feature['properties'])
        osm_tags = clean_empty_tags(osm_tags)
        geojson['features'][index]['properties'] = osm_tags
