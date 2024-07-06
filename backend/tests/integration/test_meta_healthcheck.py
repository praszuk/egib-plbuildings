from backend.areas.config import all_areas
from backend.areas.data.healtcheck_all_areas_buildings import all_areas_data as all_areas_hc_data
from backend.areas.data.healtcheck_all_areas_buildings import counties as counties_hc_data


def test_meta_config_counties_have_building_test():
    """
    Meta test to check if all config areas have defined test for e2e tests
    areas config – tests data
    """
    assert len(all_areas) == len(all_areas_hc_data)
    assert all(test_data_county.teryt in all_areas for test_data_county in counties_hc_data)
