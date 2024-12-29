from math import floor

import pytest

from backend.areas.parsers import GeoportalAreaParser

area = GeoportalAreaParser('test_area')


class TestBasicBuilding:
    @pytest.fixture(scope='class')
    def gml_content(self, load_gml):
        return load_gml('geoportal', 'gml_building_2180_crs.xml')

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

    def test_parse_broken_gml_with_special_character(self, gml_content):
        assert '<ms:ID_BUDYNKU>020101_1.0009.522_BUD</ms:ID_BUDYNKU>' in gml_content
        gml_content = gml_content.replace(
            '<ms:ID_BUDYNKU>020101_1.0009.522_BUD</ms:ID_BUDYNKU>',
            '<ms:ID_BUDYNKU>020101_1.0009.522_BUD</ms:ID_BUDYNKU>',
        )
        geojson = area.parse_gml_to_geojson(gml_content)

        assert len(geojson['features']) != 0
