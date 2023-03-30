import pytest

from os import path

from exceptions import InvalidKeyParserError
from parsers.parser_epodgik import epodgik_parser
from utils import gml_to_geojson


EXPECTED_KEYS = {'building', 'building:levels', 'building:levels:underground'}


def test_empty_params_raises_invalid_key_parser_error():
    with pytest.raises(InvalidKeyParserError):
        epodgik_parser({})


def test_only_funkcja_attribute_in_params():
    tags = epodgik_parser({'FUNKCJA': 'i'})
    assert 'building' in tags
    assert len(tags) == 1


def test_all_available_attributes_with_basic_building(test_data_dir):
    filename = path.join(test_data_dir, 'gml_basic_building.xml')
    with open(filename, 'r') as f:
        gml_data = f.read()

    geojson = gml_to_geojson(gml_data)

    tags = epodgik_parser(geojson['features'][0]['properties'])
    assert len(tags) == 3
    assert EXPECTED_KEYS == tags.keys()
