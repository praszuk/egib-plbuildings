import json
import pytest

from os import path

from backend.areas.finder import find_nearest_feature


class TestFindNearestFeature:
    @pytest.fixture(scope='class')
    def geojson(self, test_data_dir):
        return json.load(open(path.join(test_data_dir, 'find_nearest_feature.geojson')))

    def test_point_in_polygon(self, geojson):
        assert find_nearest_feature(53.7750769, 21.7385155, geojson)['properties']['ref'] == '1'
        assert find_nearest_feature(53.7748597, 21.7388094, geojson)['properties']['ref'] == '2'

    def test_point_nearest_polygon(self, geojson):
        assert find_nearest_feature(53.7750683, 21.7386798, geojson)['properties']['ref'] == '1'
        assert find_nearest_feature(53.7749108, 21.7387465, geojson)['properties']['ref'] == '2'
