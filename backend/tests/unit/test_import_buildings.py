import asyncio

from unittest.mock import AsyncMock, patch
from urllib.error import HTTPError

import pytest

from httpx import TimeoutException

from backend.areas.data.expected_building import AreaExpectedBuildingData, all_areas_data
from backend.areas.parsers import WarszawaAreaParser
from backend.models.building import Building
from backend.models.area_import import ResultStatus
from backend.tasks.import_buildings import area_import_attempt, ImportResult


@pytest.mark.anyio
async def test_area_import_attempt_success(db, load_gml):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = load_gml('warszawa', 'gml_multiple_polygons.xml')

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
    ) as mock_get, patch(
        'backend.tasks.import_buildings.area_finder.geometry_in_area', return_value=True
    ), patch.dict(all_areas_data, patched_all_areas_data, clear=True):
        area_parser = WarszawaAreaParser(name='test')

        import_result: ImportResult = asyncio.run(area_import_attempt(area_parser, '1465'))

        mock_get.assert_called_once_with(area_parser.build_buildings_url())

    assert import_result.status == ResultStatus.SUCCESS
    assert import_result.building_count == 10
    assert import_result.has_building_type is True
    assert import_result.has_building_levels is True
    assert import_result.has_building_levels_undg is False
    assert import_result.data_check_expected_tags == import_result.data_check_result_tags

    assert db.query(Building).count() == 10


def assert_failed(import_result: ImportResult, db):
    assert import_result.building_count == 0
    assert import_result.has_building_type is False
    assert import_result.has_building_levels is False
    assert import_result.has_building_levels_undg is False

    assert db.query(Building).count() == 0


@pytest.mark.anyio
async def test_area_import_attempt_connection_error_http_error(db):
    mock_response = AsyncMock(side_effect=HTTPError)

    with patch('backend.tasks.import_buildings.AsyncClient.get', return_value=mock_response):
        area_parser = WarszawaAreaParser(name='test')
        import_result: ImportResult = asyncio.run(area_import_attempt(area_parser, '1465'))

    assert import_result.status == ResultStatus.DOWNLOADING_ERROR
    assert_failed(import_result, db)


@pytest.mark.anyio
async def test_area_import_attempt_connection_error_timeout(db):
    mock_response = AsyncMock(side_effect=TimeoutException)

    with patch('backend.tasks.import_buildings.AsyncClient.get', return_value=mock_response):
        area_parser = WarszawaAreaParser(name='test')
        import_result: ImportResult = asyncio.run(area_import_attempt(area_parser, '1465'))

    assert import_result.status == ResultStatus.DOWNLOADING_ERROR
    assert_failed(import_result, db)


@pytest.mark.anyio
@pytest.mark.parametrize('status_code', [400, 404, 500, 501])
async def test_area_import_attempt_connection_error_invalid_status_code(db, status_code):
    mock_response = AsyncMock()
    mock_response.status_code = status_code

    with patch('backend.tasks.import_buildings.AsyncClient.get', return_value=mock_response):
        area_parser = WarszawaAreaParser(name='test')
        import_result: ImportResult = asyncio.run(area_import_attempt(area_parser, '1465'))

    assert import_result.status == ResultStatus.DOWNLOADING_ERROR
    assert_failed(import_result, db)


@pytest.mark.anyio
async def test_area_import_attempt_parsing_error_invalid_gml(db):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = '<invalid GML>'

    with patch('backend.tasks.import_buildings.AsyncClient.get', return_value=mock_response):
        area_parser = WarszawaAreaParser(name='test')
        import_result: ImportResult = asyncio.run(area_import_attempt(area_parser, '1465'))

    assert import_result.status == ResultStatus.PARSING_ERROR
    assert_failed(import_result, db)


@pytest.mark.anyio
async def test_area_import_attempt_parsing_error_no_building_in_area(db, load_gml):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = load_gml('warszawa', 'gml_multiple_polygons.xml')

    with patch('backend.tasks.import_buildings.AsyncClient.get', return_value=mock_response), patch(
        'backend.tasks.import_buildings.area_finder'
    ) as mock_area_finder:
        mock_area_finder.geometry_in_area.return_value = False
        area_parser = WarszawaAreaParser(name='test')
        import_result: ImportResult = asyncio.run(area_import_attempt(area_parser, '1465'))

    assert import_result.status == ResultStatus.PARSING_ERROR
    assert_failed(import_result, db)


@pytest.mark.anyio
async def test_area_import_attempt_empty_data_error(db, load_gml):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = load_gml('warszawa', 'gml_no_building.xml')

    with patch('backend.tasks.import_buildings.AsyncClient.get', return_value=mock_response):
        area_parser = WarszawaAreaParser(name='test')
        import_result: ImportResult = asyncio.run(area_import_attempt(area_parser, '1465'))

    assert import_result.status == ResultStatus.EMPTY_DATA_ERROR
    assert_failed(import_result, db)


@pytest.mark.anyio
async def test_area_import_attempt_data_check_error(db, load_gml):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = load_gml('warszawa', 'gml_multiple_polygons.xml')

    patched_all_areas_data = {
        '1465': AreaExpectedBuildingData(
            name='miasto Warszawa',
            teryt='1465',
            lat=52.22839,
            lon=21.01188,
            expected_tags={'building': 'office', 'building:levels': 11},
        )
    }

    with patch(
        'backend.tasks.import_buildings.AsyncClient.get', return_value=mock_response
    ) as mock_get, patch(
        'backend.tasks.import_buildings.area_finder.geometry_in_area', return_value=True
    ), patch.dict(all_areas_data, patched_all_areas_data, clear=True):
        area_parser = WarszawaAreaParser(name='test')

        import_result: ImportResult = asyncio.run(area_import_attempt(area_parser, '1465'))

        mock_get.assert_called_once_with(area_parser.build_buildings_url())

    assert import_result.status == ResultStatus.DATA_CHECK_ERROR
    assert import_result.building_count == 10
    assert import_result.has_building_type is True
    assert import_result.has_building_levels is True
    assert import_result.has_building_levels_undg is False
    assert import_result.data_check_expected_tags != import_result.data_check_result_tags

    assert db.query(Building).count() == 0


@pytest.mark.anyio
@pytest.mark.parametrize(
    'status,expected_tags,result_tags,return_value',
    [
        (ResultStatus.DOWNLOADING_ERROR, {'building': 'office'}, {}, False),
        (ResultStatus.PARSING_ERROR, {'building': 'office'}, {}, False),
        (ResultStatus.EMPTY_DATA_ERROR, {'building': 'office'}, {}, False),
        (ResultStatus.SUCCESS, {'building': 'office'}, {'building': 'office'}, False),
        # improvement checks
        (ResultStatus.DATA_CHECK_ERROR, {'building': 'office'}, None, False),
        (ResultStatus.DATA_CHECK_ERROR, {'building': 'office'}, {}, False),
        (ResultStatus.DATA_CHECK_ERROR, {'building': 'office'}, {'building': 'yes'}, False),
        (ResultStatus.DATA_CHECK_ERROR, {'building': 'office'}, {'building': 'residential'}, True),
        (
            ResultStatus.DATA_CHECK_ERROR,
            {'building': 'office'},
            {'building': 'yes', 'building:levels': 1},
            True,
        ),
        # should not be called at all
        (ResultStatus.SUCCESS, {'building': 'office'}, {'building': 'yes'}, False),
        (ResultStatus.SUCCESS, {'building': 'yes'}, {'building': 'office'}, False),
    ],
)
def test_import_result_is_data_check_error_with_improved_tags(
    status: ResultStatus, expected_tags: dict, result_tags: dict, return_value: bool
):
    import_result = ImportResult(
        teryt='1',
        status=status,
        data_check_expected_tags=expected_tags,
        data_check_result_tags=result_tags,
    )
    assert import_result.is_data_check_error_with_improved_tags() == return_value
