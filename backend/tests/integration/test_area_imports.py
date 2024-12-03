from unittest.mock import patch

import pytest

from backend.areas.parsers import BaseAreaParser
from backend.areas.config import all_areas
from backend.models.area_import import AreaImport
from backend.models.area_import import ResultStatus


@pytest.mark.anyio
@patch.dict(all_areas, {teryt: BaseAreaParser(name=teryt) for teryt in ('0001', '0002')})
async def test_list_latest_area_imports_returns_unique_areas_imports(async_client, db):
    params = {
        'start_at': '2024-01-01T00:00:00',
        'building_count': 0,
        'has_building_type': True,
        'has_building_levels': False,
        'has_building_levels_undg': False,
    }

    area_import_objects = [
        AreaImport(
            teryt='0001',
            result_status=ResultStatus.DOWNLOADING_ERROR,
            end_at='2024-01-01T00:00:01',
            **params,
        ),
        AreaImport(
            teryt='0001', result_status=ResultStatus.SUCCESS, end_at='2024-01-01T00:01:01', **params
        ),
        AreaImport(
            teryt='0002', result_status=ResultStatus.SUCCESS, end_at='2024-01-01T00:01:01', **params
        ),
        AreaImport(
            teryt='0001',
            result_status=ResultStatus.PARSING_ERROR,
            end_at='2024-01-01T00:04:01',
            **params,
        ),
        AreaImport(
            teryt='0001',
            result_status=ResultStatus.EMPTY_DATA_ERROR,
            end_at='2024-01-01T00:03:01',
            **params,
        ),
        AreaImport(
            teryt='0002',
            result_status=ResultStatus.DOWNLOADING_ERROR,
            end_at='2024-01-01T00:00:01',
            **params,
        ),
    ]
    for obj in area_import_objects:
        db.add(obj)
    db.commit()

    assert db.query(AreaImport).count() == len(area_import_objects)

    response = await async_client.get('area_imports/latest')
    assert response.status_code == 200
    result = response.json()

    assert len(result) == 2

    assert result[0]['teryt'] == '0001'
    assert result[0]['result_status'] == ResultStatus.PARSING_ERROR.value
    assert params.items() <= result[0].items()

    assert result[1]['teryt'] == '0002'
    assert result[1]['result_status'] == ResultStatus.SUCCESS.value
    assert params.items() <= result[1].items()


@pytest.mark.anyio
@patch.dict(
    all_areas, {teryt: BaseAreaParser(name=teryt) for teryt in ('0001', '0002', '0003', '0004')}
)
async def test_list_stable_area_imports_returns_latest_success_or_latest_failed(async_client, db):
    params = {
        'start_at': '2024-01-01T00:00:00',
        'has_building_type': True,
        'has_building_levels': False,
        'has_building_levels_undg': False,
    }

    area_import_objects = [
        AreaImport(
            teryt='0001',
            result_status=ResultStatus.DOWNLOADING_ERROR,
            building_count=0,
            end_at='2024-01-01T00:00:01',
            **params,
        ),
        AreaImport(
            teryt='0001',
            result_status=ResultStatus.SUCCESS,
            building_count=2,
            end_at='2024-01-01T00:02:01',
            **params,
        ),
        AreaImport(
            teryt='0001',
            result_status=ResultStatus.SUCCESS,
            building_count=1,
            end_at='2024-01-01T00:01:01',
            **params,
        ),
        AreaImport(
            teryt='0002',
            result_status=ResultStatus.SUCCESS,
            building_count=0,
            end_at='2024-01-01T00:00:01',
            **params,
        ),
        AreaImport(
            teryt='0002',
            result_status=ResultStatus.PARSING_ERROR,
            building_count=1,
            end_at='2024-01-01T00:01:01',
            **params,
        ),
        AreaImport(
            teryt='0003',
            result_status=ResultStatus.DOWNLOADING_ERROR,
            building_count=0,
            end_at='2024-01-01T00:00:01',
            **params,
        ),
        AreaImport(
            teryt='0003',
            result_status=ResultStatus.PARSING_ERROR,
            building_count=1,
            end_at='2024-01-01T00:01:01',
            **params,
        ),
        AreaImport(
            teryt='0003',
            result_status=ResultStatus.DOWNLOADING_ERROR,
            building_count=3,
            end_at='2024-01-01T00:03:01',
            **params,
        ),
        AreaImport(
            teryt='0003',
            result_status=ResultStatus.EMPTY_DATA_ERROR,
            building_count=2,
            end_at='2024-01-01T00:02:01',
            **params,
        ),
        AreaImport(
            teryt='0004',
            result_status=ResultStatus.DOWNLOADING_ERROR,
            building_count=0,
            end_at='2024-01-01T00:00:01',
            **params,
        ),
    ]
    for obj in area_import_objects:
        db.add(obj)
    db.commit()
    assert db.query(AreaImport).count() == len(area_import_objects)

    response = await async_client.get('area_imports/stable')
    assert response.status_code == 200
    result = response.json()

    assert len(result) == 4
    teryt_result = {r['teryt']: r for r in result}

    assert teryt_result['0001']['building_count'] == 2
    assert teryt_result['0002']['building_count'] == 0
    assert teryt_result['0003']['building_count'] == 3
    assert teryt_result['0004']['building_count'] == 0
