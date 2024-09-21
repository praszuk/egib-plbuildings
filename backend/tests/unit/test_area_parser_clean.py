import pytest

from backend.areas.parsers import WroclawAreaParser

area = WroclawAreaParser('test_area', 'test_url_code')


class TestBuildingIncorrectLevelsValues:
    def test_tags_have_no_numerical_building_levels(self):
        osm_tags = {
            'building': 'office',
            'building:levels': 'brak uprawnień',
            'building:levels:underground': 'brak uprawnień',
        }
        cleaned_tags = area.clean_tags(osm_tags)
        assert cleaned_tags == {'building': 'office'}

    @pytest.mark.parametrize(
        'levels,underground_levels', [(0, 0), (-1, -2), ('0', '0'), ('-1', '-2')]
    )
    def test_tags_have_numerical_non_positive_building_levels(self, levels, underground_levels):
        osm_tags = {
            'building': 'office',
            'building:levels': levels,
            'building:levels:underground': underground_levels,
        }
        cleaned_tags = area.clean_tags(osm_tags)
        assert cleaned_tags == {'building': 'office'}
