import json
from os import path

import pytest

from backend.areas.config import all_areas
from backend.areas.healthcheck import ALL_AREAS_DATA_FILENAME


@pytest.fixture(scope='class')
def counties_coordinates_buildings(project_data_dir) -> dict:
    filename = path.join(project_data_dir, ALL_AREAS_DATA_FILENAME)
    return json.load(open(filename, 'r'))


def test_meta_config_counties_have_building_test(counties_coordinates_buildings):
    """
    Meta test to check if all config areas have defined test for e2e tests
    areas config – tests data
    """
    assert len(all_areas) == len(counties_coordinates_buildings)
    assert all(
        test_data_county['teryt'] in all_areas
        for test_data_county in counties_coordinates_buildings
    )
