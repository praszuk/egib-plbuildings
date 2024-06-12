from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict

from osgeo import ogr  # noqa


@dataclass(frozen=True)
class County:
    name: str
    data_parser: Callable  # type: ignore
    url_builder: Callable  # type: ignore
    url_extras: Dict[str, Any]

    def build_url(self, lat: float, lon: float) -> str:
        return self.url_builder(self, lat=lat, lon=lon)  # type: ignore


@dataclass(frozen=True)
class CountyGeometry:
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


@dataclass(frozen=True)
class HealthCheckCountyReport:
    status_code: int
    is_building_data: bool = False
    is_expected_building_data: bool = False


@dataclass(frozen=True)
class HealthCheckReport:
    start_dt: str
    end_dt: str
    counties: Dict[str, HealthCheckCountyReport]
