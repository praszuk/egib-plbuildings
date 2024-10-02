from math import floor

import pytest

from backend.areas.parsers import GeoportalAreaParser

area = GeoportalAreaParser('test_area', custom_crs=2180)


class TestBasicBuilding:
    @pytest.fixture(scope='class')
    def gml_content(self, load_geoportal_gml):
        return load_geoportal_gml('gml_building_2180_crs.xml')

    @pytest.fixture(scope='class')
    def geojson(self, gml_content):
        return area.parse_gml_to_geojson(gml_content)

    def test_coordinates_reprojected_to_4326(self, geojson):
        lon, lat = geojson['features'][0]['geometry']['coordinates'][0][0]

        assert (floor(lat * 1000) / 1000) == 51.262
        assert (floor(lon * 1000) / 1000) == 15.568

    def test_geojson_coordinates_first_and_last_eq(self, geojson):
        first = geojson['features'][0]['geometry']['coordinates'][0][0]
        last = geojson['features'][0]['geometry']['coordinates'][0][-1]
        assert first == last
