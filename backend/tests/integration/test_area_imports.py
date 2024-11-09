import pytest

from backend.models.area_import import AreaImport
from backend.models.area_import import ResultStatus


@pytest.mark.anyio
async def test_list_latest_area_imports_returns_unique_areas_imports(async_client, db):
    params = {
        'start_at': '2024-01-01T00:00:00',
        'end_at': '2024-01-01T00:00:01',
        'building_count': 0,
        'has_building_type': True,
        'has_building_levels': False,
        'has_building_levels_undg': False,
    }

    area_import_objects = [
        AreaImport(teryt='0001', result_status=ResultStatus.DOWNLOADING_ERROR, **params),
        AreaImport(teryt='0001', result_status=ResultStatus.SUCCESS, **params),
        AreaImport(teryt='0002', result_status=ResultStatus.SUCCESS, **params),
        AreaImport(teryt='0001', result_status=ResultStatus.PARSING_ERROR, **params),
    ]
    for obj in area_import_objects:
        db.add(obj)
    db.commit()

    assert db.query(AreaImport).count() == 4

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
