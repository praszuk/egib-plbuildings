import pytest

from backend.areas.parsers import EpodgikAreaParser


area = EpodgikAreaParser('test_area', 'test_url_code')


class TestNoBuildingData:
    @pytest.fixture(scope='class')
    def gml_content(self, load_epodgik_gml):
        return load_epodgik_gml('gml_no_building.xml')

    def test_empty_geojson(self, gml_content):
        geojson = area.parse_gml_to_geojson(gml_content)
        assert len(geojson['features']) == 0


class TestBasicBuilding:
    @pytest.fixture(scope='class')
    def gml_content(self, load_epodgik_gml):
        return load_epodgik_gml('gml_basic_building.xml')

    @pytest.fixture(scope='class')
    def geojson(self, gml_content):
        return area.parse_gml_to_geojson(gml_content)

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
            'KONDYGNACJE_PODZIEMNE': None,
        }
        assert geojson['features'][0]['properties'] == expected_properties


class TestMultipleBuildings:
    @pytest.fixture(scope='class')
    def gml_content(self, load_epodgik_gml):
        return load_epodgik_gml('gml_multiple_buildings.xml')

    @pytest.fixture(scope='class')
    def geojson(self, gml_content):
        return area.parse_gml_to_geojson(gml_content)

    def test_geojson_has_three_features(self, geojson):
        assert len(geojson['features']) == 3

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


class TestCoordinatesCorrectOrderAutoFix:
    @pytest.mark.parametrize(
        'test_filename',
        [
            'gml_coordinates_lat_lon_order.xml',
            'gml_coordinates_lon_lat_order.xml',
        ],
    )
    def test_lon_lat_as_geojson(self, load_epodgik_gml, test_filename):
        gml_content = load_epodgik_gml(test_filename)
        geojson = area.parse_gml_to_geojson(gml_content)
        point = geojson['features'][0]['geometry']['coordinates'][0][0]

        assert point[0] < point[1]
