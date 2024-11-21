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

    hc_has_expected_tags: bool
    hc_expected_tags: dict[str, Any] | None
    hc_result_tags: dict[str, Any] | None
