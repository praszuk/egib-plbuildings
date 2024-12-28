import asyncio

from unittest.mock import patch

import pytest


from backend.areas.config import all_counties
from backend.models.area_import import ResultStatus
from backend.tasks.import_buildings import (
    area_import_in_parallel,
    ImportResult,
)


@pytest.mark.anyio
def test_failed_two_attempts_downloading_error_then_success(db):
    with patch('backend.tasks.import_buildings.SessionLocal', return_value=db):
        with patch(
            'backend.tasks.import_buildings.area_import_attempt',
            side_effect=[
                ImportResult(teryt='123', status=ResultStatus.DOWNLOADING_ERROR),
                ImportResult(teryt='123', status=ResultStatus.SUCCESS),
            ],
        ) as mock_area_attempt_func:
            asyncio.run(
                area_import_in_parallel(
                    [list(all_counties.keys())[0]],
                    delay_between_attempts=0.001,
                    max_attempts_per_area=3,
                )
            )
            assert mock_area_attempt_func.call_count == 2


@pytest.mark.anyio
def test_failed_one_attempt_but_with_parameter_to_max_one_attempt(db):
    with patch('backend.tasks.import_buildings.SessionLocal', return_value=db):
        with patch(
            'backend.tasks.import_buildings.area_import_attempt',
            side_effect=[ImportResult(teryt='123', status=ResultStatus.DOWNLOADING_ERROR)],
        ) as mock_area_attempt_func:
            asyncio.run(
                area_import_in_parallel(
                    [list(all_counties.keys())[0]],
                    delay_between_attempts=0.001,
                    max_attempts_per_area=1,
                )
            )
            assert mock_area_attempt_func.call_count == 1


@pytest.mark.anyio
def test_failed_data_check_error_three_attempts_no_tags_improvement(db):
    with patch('backend.tasks.import_buildings.SessionLocal', return_value=db):
        with patch(
            'backend.tasks.import_buildings.area_import_attempt',
            side_effect=[ImportResult(teryt='123', status=ResultStatus.DATA_CHECK_ERROR)] * 5,
        ) as mock_area_attempt_func:
            asyncio.run(
                area_import_in_parallel(
                    [list(all_counties.keys())[0]], delay_between_attempts=0.001
                )
            )
            assert mock_area_attempt_func.call_count == 5


@pytest.mark.anyio
def test_failed_data_check_error_one_attempt_tags_improvement(db):
    with patch('backend.tasks.import_buildings.SessionLocal', return_value=db):
        with patch(
            'backend.tasks.import_buildings.area_import_attempt',
            side_effect=[ImportResult(teryt='123', status=ResultStatus.DATA_CHECK_ERROR)],
        ) as mock_area_attempt_func, patch(
            'backend.tasks.import_buildings.ImportResult.is_data_check_error_with_improved_tags',
            return_value=True,
        ):
            asyncio.run(
                area_import_in_parallel(
                    [list(all_counties.keys())[0]], delay_between_attempts=0.001
                )
            )
            assert mock_area_attempt_func.call_count == 1
