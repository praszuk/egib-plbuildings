import pytest

from backend.exceptions import InvalidKeyParserError
from backend.parsers.parser_epodgik import epodgik_parser
from backend.utils import gml_to_geojson

EXPECTED_KEYS = {'building', 'building:levels', 'building:levels:underground'}


def test_empty_params_raises_invalid_key_parser_error():
    with pytest.raises(InvalidKeyParserError):
        epodgik_parser({})


def test_only_funkcja_attribute_in_params():
    tags = epodgik_parser({'FUNKCJA': 'i'})
    assert 'building' in tags
    assert len(tags) == 1


def test_all_available_attributes_with_basic_building(load_gml):
    gml_data = load_gml('gml_basic_building.xml')
    geojson = gml_to_geojson(gml_data)

    tags = epodgik_parser(geojson['features'][0]['properties'])
    assert len(tags) == 3
    assert EXPECTED_KEYS == tags.keys()
