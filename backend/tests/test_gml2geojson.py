import pytest

from os import path
from ..utils import gml_to_geojson


class TestNoBuildingData:
    @pytest.fixture(scope='class')
    def gml_content(self, test_data_dir):
        filename = path.join(test_data_dir, 'gml_no_building.xml')
        with open(filename, 'r') as f:
            return f.read()

    def test_empty_geojson(self, gml_content):
        geojson = gml_to_geojson(gml_content)
        assert len(geojson['features']) == 0


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

    def test_geojson_has_all_properties(self, geojson):
        expected_properties = {
            'FUNKCJA': 'i',
            'KONDYGNACJE_NADZIEMNE': '3',
            'RODZAJ': 'ognioodporny',
            'ID_BUDYNKU': '142104_2.0013.628/16.1_BUD',
            'KONDYGNACJE_PODZIEMNE': ''
        }
        assert geojson['features'][0]['properties'] == expected_properties


class TestMultipleBuildings:
    @pytest.fixture(scope='class')
    def gml_content(self, test_data_dir):
        filename = path.join(test_data_dir, 'gml_multiple_buildings.xml')
        with open(filename, 'r') as f:
            return f.read()

    @pytest.fixture(scope='class')
    def geojson(self, gml_content):
        return gml_to_geojson(gml_content)

    def test_geojson_has_three_features(self, geojson):
        assert len(geojson['features']) == 3

    def test_geojson_features_have_different_geometries(self, geojson):
        geometries = set()
        for feature in geojson['features']:
            geometries.add(str(feature['geometry']['coordinates']))

        assert len(geometries) == len(geojson['features'])
