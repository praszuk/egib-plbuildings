from backend.areas.config import all_areas
from backend.areas.data.expected_building import (
    all_areas_data as all_areas_hc_data,
    counties as counties_hc_data,
)


def test_config_areas_have_building_hc_test():
    assert len(all_areas) == len(all_areas_hc_data)
    assert all(test_data_teryt in all_areas for test_data_teryt in counties_hc_data.keys())


def test_hc_data_area_expected_building_key_and_obj_attr_are_equal():
    assert all(teryt == area.teryt for teryt, area in all_areas_hc_data.items())
