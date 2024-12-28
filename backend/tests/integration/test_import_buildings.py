import asyncio
import pytest
from unittest.mock import AsyncMock, patch

from backend.areas.data.expected_building import all_areas_data, AreaExpectedBuildingData
from backend.areas.parsers import WarszawaAreaParser
from backend.models.building import Building
from backend.models.area_import import AreaImport, ResultStatus
from backend.tasks.import_buildings import area_import_in_parallel


@pytest.mark.anyio
async def test_area_import_in_parallel_success(db, load_warszawa_gml):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = load_warszawa_gml('gml_multiple_polygons.xml')

    patched_all_areas_data = {
        '1465': AreaExpectedBuildingData(
            name='miasto Warszawa',
            teryt='1465',
            lat=52.22839,
            lon=21.01188,
            expected_tags={'building': 'office', 'building:levels': 12},
        )
    }

    with patch(
        'backend.tasks.import_buildings.AsyncClient.get', return_value=mock_response
    ) as mock_get, patch('backend.tasks.import_buildings.SessionLocal', return_value=db), patch(
        'backend.tasks.import_buildings.area_finder.geometry_in_area', return_value=True
    ), patch.dict(all_areas_data, patched_all_areas_data, clear=True):
        area_parser = WarszawaAreaParser(name='test')

        asyncio.run(area_import_in_parallel(teryt_ids=['1465']))

        mock_get.assert_called_once_with(area_parser.build_buildings_url())

    area_import = db.query(AreaImport).first()
    expected_data = patched_all_areas_data['1465']
    assert area_import.result_status == ResultStatus.SUCCESS
    assert area_import.teryt == '1465'
    assert area_import.start_at < area_import.end_at
    assert area_import.has_building_type is True
    assert area_import.has_building_levels is True
    assert area_import.has_building_levels_undg is False
    assert area_import.data_check_lat == expected_data.lat
    assert area_import.data_check_lon == expected_data.lon
    assert area_import.data_check_expected_tags == expected_data.expected_tags
    assert area_import.data_check_result_tags == area_import.data_check_expected_tags
    assert area_import.data_check_has_expected_tags == True
    assert area_import.building_count == 10
    assert db.query(Building).count() == 10


@pytest.mark.anyio
async def test_area_import_in_parallel_data_check_failed_building_not_found(db, load_warszawa_gml):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = load_warszawa_gml('gml_multiple_polygons.xml')

    patched_all_areas_data = {
        '1465': AreaExpectedBuildingData(
            name='miasto Warszawa',
            teryt='1465',
            lat=52.00,
            lon=21.00,
            expected_tags={'building': 'office', 'building:levels': 12},
        )
    }

    with patch(
        'backend.tasks.import_buildings.AsyncClient.get', return_value=mock_response
    ) as mock_get, patch(
        'backend.tasks.import_buildings.SessionLocal', return_value=db
    ), patch.dict(all_areas_data, patched_all_areas_data, clear=True), patch(
        'backend.tasks.import_buildings.area_finder.geometry_in_area', return_value=True
    ):
        area_parser = WarszawaAreaParser(name='test')
        asyncio.run(area_import_in_parallel(teryt_ids=['1465'], delay_between_attempts=0.0001))
        mock_get.assert_called_with(area_parser.build_buildings_url())
        assert mock_get.call_count == 5

    area_import = db.query(AreaImport).first()
    expected_data = patched_all_areas_data['1465']
    assert area_import.result_status == ResultStatus.DATA_CHECK_ERROR
    assert area_import.start_at < area_import.end_at
    assert area_import.teryt == '1465'
    assert area_import.has_building_type is True
    assert area_import.has_building_levels is True
    assert area_import.has_building_levels_undg is False
    assert area_import.data_check_lat == expected_data.lat
    assert area_import.data_check_lon == expected_data.lon
    assert area_import.data_check_expected_tags == expected_data.expected_tags
    assert area_import.data_check_result_tags is None
    assert area_import.data_check_has_expected_tags == False
    assert area_import.building_count == 10
    assert db.query(Building).count() == 0
