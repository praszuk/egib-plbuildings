from backend.areas.parsers import KatowiceAreaParser, WarszawaAreaParser


class TestGmlToGeojsonParser:
    def test_multisurface_with_many_polygons_produces_many_features(self, load_warszawa_gml):
        gml_content = load_warszawa_gml('gml_multisurface_multiple_polygons.xml')
        geojson = WarszawaAreaParser(name='test').parse_gml_to_geojson(gml_content)
        assert len(geojson['features']) == 2

    def test_gml_3d_flatten_to_2d(self, load_katowice_gml):
        gml_content = load_katowice_gml('gml_basic_building_3d.xml')
        geojson = KatowiceAreaParser(name='').parse_gml_to_geojson(gml_content)
        assert len(geojson['features'][0]['geometry']['coordinates'][0][0]) == 2
