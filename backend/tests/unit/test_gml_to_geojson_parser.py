from backend.areas.parsers import WarszawaAreaParser


class TestGmlToGeojsonParser:
    def test_multisurface_with_many_polygons_produces_many_features(self, load_warszawa_gml):
        gml_content = load_warszawa_gml('gml_multisurface_multiple_polygons.xml')
        geojson = WarszawaAreaParser(name='test').parse_gml_to_geojson(gml_content)
        assert len(geojson['features']) == 2
