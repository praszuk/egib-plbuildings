from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class HealthCheckTestAreaData:
    teryt: str
    name: str
    lat: float
    lon: float
    expected_tags: Dict[str, Any]


@dataclass(frozen=True)
class HealthCheckAreaReport:
    test_area_data: HealthCheckTestAreaData
    status_code: int
    has_building_data: bool = False
    has_expected_building_data: bool = False
    result_tags: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class HealthCheckReport:
    start_dt: str
    end_dt: str
    counties: Dict[str, HealthCheckAreaReport]
    communes: Dict[str, HealthCheckAreaReport]
