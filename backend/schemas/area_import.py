from datetime import datetime

from typing import Any

from pydantic import BaseModel

from backend.models.area_import import ResultStatus


class AreaImport(BaseModel):
    id: int
    name: str
    teryt: str

    start_at: datetime
    end_at: datetime
    result_status: ResultStatus

    building_count: int

    has_building_type: bool
    has_building_levels: bool
    has_building_levels_undg: bool

    data_check_has_expected_tags: bool
    data_check_expected_tags: dict[str, Any] | None
    data_check_result_tags: dict[str, Any] | None
