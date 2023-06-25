import json
from os import path

import pytest

from backend.powiats.config import all_powiats
from backend.powiats.healthcheck import ALL_POWIATS_DATA_FILENAME


@pytest.fixture(scope='class')
def powiats_coordinates_buildings(project_data_dir) -> dict:
    filename = path.join(project_data_dir, ALL_POWIATS_DATA_FILENAME)
    return json.load(open(filename, 'r'))


def test_meta_config_powiats_have_building_test(powiats_coordinates_buildings):
    """
    Meta test to check if all config powiats have defined test for e2e tests
    powiats config – tests data
    """
    assert len(all_powiats) == len(powiats_coordinates_buildings)
    assert all(
        test_data_powiat['teryt'] in all_powiats
        for test_data_powiat in powiats_coordinates_buildings
    )
