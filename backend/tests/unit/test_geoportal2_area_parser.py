import pytest

from backend.areas.parsers import Geoportal2AreaParser, DEFAULT_BUILDING

area = Geoportal2AreaParser('test_area', 'test_url_code')


class TestNoBuildingData:
    @pytest.fixture(scope='class')
    def gml_content(self, load_geoportal2_gml):
        return load_geoportal2_gml('gml_no_building.xml')

    def test_empty_geojson(self, gml_content):
        geojson = area.parse_gml_to_geojson(gml_content)
        assert len(geojson['features']) == 0


class TestBasicBuilding:
    @pytest.fixture(scope='class')
    def gml_content(self, load_geoportal2_gml):
        return load_geoportal2_gml('gml_basic_building.xml')

    @pytest.fixture(scope='class')
    def geojson(self, gml_content):
        return area.parse_gml_to_geojson(gml_content)

    def test_geojson_has_one_feature(self, geojson):
        assert len(geojson['features']) == 1

    def test_geojson_has_17_coordinates(self, geojson):
        assert len(geojson['features'][0]['geometry']['coordinates'][0]) == 17

    def test_geojson_coordinates_first_and_last_eq(self, geojson):
        first = geojson['features'][0]['geometry']['coordinates'][0][0]
        last = geojson['features'][0]['geometry']['coordinates'][0][-1]
        assert first == last

    def test_geojson_has_all_properties(self, geojson):
        expected_properties = {
            'RODZAJ': 'b',
            'ID_BUDYNKU': '240301_1.0033.2_BUD',
        }
        assert geojson['features'][0]['properties'] == expected_properties


class TestBuildingNoBuildingType:
    @pytest.fixture(scope='class')
    def gml_content(self, load_geoportal2_gml):
        return load_geoportal2_gml('gml_building_no_building_type.xml')

    @pytest.fixture(scope='class')
    def geojson(self, gml_content):
        return area.parse_gml_to_geojson(gml_content)

    def test_geojson_parsed_to_default_building_value(self, geojson):
        tags = area.parse_feature_properties_to_osm_tags(geojson)
        assert tags == {'building': DEFAULT_BUILDING}


class TestMultipleBuildings:
    @pytest.fixture(scope='class')
    def gml_content(self, load_geoportal2_gml):
        return load_geoportal2_gml('gml_multiple_buildings.xml')

    @pytest.fixture(scope='class')
    def geojson(self, gml_content):
        return area.parse_gml_to_geojson(gml_content)

    def test_geojson_has_three_features(self, geojson):
        assert len(geojson['features']) == 2

    def test_geojson_features_have_different_geometries(self, geojson):
        geometries = set()
        for feature in geojson['features']:
            geometries.add(str(feature['geometry']['coordinates']))

        assert len(geometries) == len(geojson['features'])

    def test_geojson_features_have_different_ids(self, geojson):
        ids = set()
        for feature in geojson['features']:
            ids.add(str(feature['properties']['ID_BUDYNKU']))

        assert len(ids) == len(geojson['features'])
