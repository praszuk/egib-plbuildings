from typing import Any, Dict, Final

from backend.exceptions import ParserNotFound
from backend.parsers.parser_epodgik import epodgik_parser

TERYT_PARSER: Final = {
    '1421': epodgik_parser,
}


def egib_to_osm(geojson: Dict[str, Any], teryt: str) -> None:
    """
    Change EGiB properties to OSM tags
    :param geojson: raw EGIB GeoJSON from one wfs service/powiat
    :param teryt: 4 numbers powiat (county) code as str
    :raises ParserNotFound, InvalidKeyParserError, ParserError:
    """
    try:
        parser = TERYT_PARSER[teryt]
    except KeyError:
        raise ParserNotFound(teryt)

    for index, feature in enumerate(geojson['features']):
        osm_tags = parser(feature['properties'])
        geojson['features'][index]['properties'] = osm_tags
