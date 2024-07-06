import pytest

from backend.areas.parsers import WroclawAreaParser

area = WroclawAreaParser('test_area', 'test_url_code')


class TestBuildingIncorrectLevelsValues:
    @pytest.fixture(scope='class')
    def gml_content(self, load_other_gml):
        return load_other_gml('gml_building_incorrect_levels_value.xml')

    @pytest.fixture(scope='class')
    def geojson(self, gml_content):
        return area.parse_gml_to_geojson(gml_content)

    def test_geojson_parsed_has_no_incorrect_building_values(self, geojson):
        area.replace_properties_with_osm_tags(geojson)
        tags = geojson['features'][0]['properties']
        assert tags == {'building': 'office'}
