from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from osgeo import ogr, osr  # noqa
from abc import ABC


@dataclass(frozen=True)
class Area(ABC):
    name: str
    url_code: str


@dataclass(frozen=True)
class AreaGeometry:
    """
    Wrapper class for OGR Geometry to handle serialization properly.
    """

    geom: ogr.Geometry

    # __getstate__ and __setstate__ are not needed at all, but without them
    # GDAL prints errors on deserialization
    # 'ERROR 1: Empty geometries cannot be constructed'
    def __getstate__(self) -> Dict[str, Any]:
        return {'geom': self.geom.ExportToWkb()}

    def __setstate__(self, state: Dict[str, Any]) -> None:
        object.__setattr__(self, 'geom', ogr.CreateGeometryFromWkb(state['geom']))


@dataclass
class HealtCheckTestAreaData:
    teryt: str
    name: str
    lat: float
    lon: float
    expected_tags: Dict[str, Any]


@dataclass(frozen=True)
class HealthCheckAreaReport:
    test_area_data: HealtCheckTestAreaData
    status_code: int
    is_building_data: bool = False
    is_expected_building_data: bool = False
    result_tags: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class HealthCheckReport:
    start_dt: str
    end_dt: str
    counties: Dict[str, HealthCheckAreaReport]
    communes: Dict[str, HealthCheckAreaReport]
