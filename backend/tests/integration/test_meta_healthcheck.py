import json
from os import path

import pytest

from backend.counties.config import all_counties
from backend.counties.healthcheck import ALL_COUNTIES_DATA_FILENAME


@pytest.fixture(scope='class')
def counties_coordinates_buildings(project_data_dir) -> dict:
    filename = path.join(project_data_dir, ALL_COUNTIES_DATA_FILENAME)
    return json.load(open(filename, 'r'))


def test_meta_config_counties_have_building_test(
    counties_coordinates_buildings,
):
    """
    Meta test to check if all config counties have defined test for e2e tests
    counties config – tests data
    """
    assert len(all_counties) == len(counties_coordinates_buildings)
    assert all(
        test_data_county['teryt'] in all_counties
        for test_data_county in counties_coordinates_buildings
    )
