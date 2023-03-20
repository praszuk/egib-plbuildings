import pytest

from os import path
from ..utils import gml_to_geojson


class TestBasicBuilding:
    @pytest.fixture(scope='class')
    def gml_content(self, test_data_dir):
        filename = path.join(test_data_dir, 'gml_basic_building.xml')
        with open(filename, 'r') as f:
            return f.read()

    @pytest.fixture(scope='class')
    def geojson(self, gml_content):
        return gml_to_geojson(gml_content)

    def test_geojson_has_one_feature(self, geojson):
        assert len(geojson['features']) == 1

    def test_geojson_has_22_coordinates(self, geojson):
        assert len(geojson['features'][0]['geometry']['coordinates'][0]) == 22

    def test_geojson_coordinates_first_and_last_eq(self, geojson):
        first = geojson['features'][0]['geometry']['coordinates'][0][0]
        last = geojson['features'][0]['geometry']['coordinates'][0][-1]
        assert first == last
