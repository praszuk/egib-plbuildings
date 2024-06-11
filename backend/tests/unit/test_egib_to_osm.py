import pytest

from backend.counties.egib_to_osm import egib_to_osm
from backend.counties.parsers.utils import gml_to_geojson
from backend.exceptions import CountyNotSupported


@pytest.fixture(scope='class')
def gml_content(load_gml):
    return load_gml('gml_multiple_buildings.xml')


@pytest.fixture(scope='function')
def geojson(gml_content):
    return gml_to_geojson(gml_content)


def test_multiple_building_exists_county(geojson):
    assert not any('building' in f['properties'] for f in geojson['features'])
    egib_to_osm(geojson, '1421')  # data files using 1421 – "pruszkowski"
    assert all('building' in f['properties'] for f in geojson['features'])


def test_multiple_building_in_not_exists_county_raise_error(geojson):
    assert not any('building' in f['properties'] for f in geojson['features'])

    with pytest.raises(CountyNotSupported):
        egib_to_osm(geojson, '0000')

    assert not any('building' in f['properties'] for f in geojson['features'])
