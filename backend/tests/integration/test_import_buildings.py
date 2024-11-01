import asyncio
import pytest
from unittest.mock import AsyncMock, patch

from backend.areas.parsers import WarszawaAreaParser
from backend.models.building import Building
from backend.models.area_import import AreaImport, ResultStatus
from backend.tasks.import_buildings import area_import_in_parallel


@pytest.mark.anyio
async def test_area_import(db, load_warszawa_gml):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.text = load_warszawa_gml('gml_multiple_polygons.xml')

    with patch(
        'backend.tasks.import_buildings.AsyncClient.get', return_value=mock_response
    ) as mock_get, patch('backend.tasks.import_buildings.SessionLocal', return_value=db):
        area_parser = WarszawaAreaParser(name='test')

        asyncio.run(area_import_in_parallel(teryt_ids=['1465']))

        mock_get.assert_called_once_with(area_parser.build_buildings_url())

    area_import = db.query(AreaImport).first()
    assert area_import.result_status == ResultStatus.SUCCESS
    assert area_import.teryt == '1465'
    assert area_import.start_at < area_import.end_at
    assert area_import.has_building_type is True
    assert area_import.has_building_levels is True
    assert area_import.has_building_levels_undg is False
    assert area_import.building_count == 10
    assert db.query(Building).count() == 10
