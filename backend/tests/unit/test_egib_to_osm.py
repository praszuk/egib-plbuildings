import pytest

from backend.exceptions import ParserNotFound
from backend.parsers.egib_to_osm import egib_to_osm
from backend.utils import gml_to_geojson


@pytest.fixture(scope='class')
def gml_content(load_gml):
    return load_gml('gml_multiple_buildings.xml')


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
