from typing import Any, Dict

from exceptions import InvalidKeyParserError
from .parser_default import DEFAULT_BUILDING, BUILDING_KST_CODE_TYPE


def epodgik_parser(properties: Dict[str, Any]) -> Dict[str, Any]:
    """
    EPODGIK key-values mapping from WFS
    :param properties: GeoJSON raw properties
    :return: OSM tags
    """
    tags = {}

    try:
        tags['building'] = BUILDING_KST_CODE_TYPE.get(
            properties['FUNKCJA'],
            DEFAULT_BUILDING
        )
        if 'KONDYGNACJE_NADZIEMNE' in properties:
            tags['building:levels'] = properties.get('KONDYGNACJE_NADZIEMNE')

        if 'KONDYGNACJE_PODZIEMNE' in properties:
            tags['building:levels:underground'] = properties.get(
                'KONDYGNACJE_PODZIEMNE'
            )

        # RODZAJ and ID_BUDYNKU skipped

    except KeyError as e:
        raise InvalidKeyParserError(e)

    return tags
