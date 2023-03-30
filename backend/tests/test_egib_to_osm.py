import pytest

from os import path

from exceptions import ParserNotFound
from parsers.egib_to_osm import egib_to_osm
from utils import gml_to_geojson


@pytest.fixture(scope='class')
def gml_content(test_data_dir):
    filename = path.join(test_data_dir, 'gml_multiple_buildings.xml')
    with open(filename, 'r') as f:
        return f.read()


@pytest.fixture(scope='function')
def geojson(gml_content):
    return gml_to_geojson(gml_content)


def test_multiple_building_exists_powiat(geojson):
    assert not any('building' in f['properties'] for f in geojson['features'])
    egib_to_osm(geojson, '1421')  # data files using 1421 – powiat pruszkowski
    assert all('building' in f['properties'] for f in geojson['features'])


def test_multiple_building_in_not_exists_powiat_raise_error(geojson):
    assert not any('building' in f['properties'] for f in geojson['features'])

    with pytest.raises(ParserNotFound):
        egib_to_osm(geojson, '0000')

    assert not any('building' in f['properties'] for f in geojson['features'])
