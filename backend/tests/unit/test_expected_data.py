import pytest

from backend.areas.config import all_areas
from backend.areas.data.expected_building import (
    all_areas_data as all_dc_areas,
    counties as counties_dc,
)


def test_config_areas_have_building_dc():
    assert len(all_areas) == len(all_dc_areas)
    assert all(test_data_teryt in all_areas for test_data_teryt in counties_dc.keys())


def test_dc_area_expected_building_key_and_obj_attr_are_equal():
    assert all(teryt == area.teryt for teryt, area in all_dc_areas.items())


@pytest.mark.anyio
@pytest.mark.parametrize(
    'expected_teryt,lat,lon', [(teryt, area.lat, area.lon) for teryt, area in all_dc_areas.items()]
)
def test_dc_area_lat_lon_points_correct_area(area_finder, expected_teryt, lat, lon):
    assert area_finder.area_at(lat, lon) == expected_teryt
