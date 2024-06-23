from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from osgeo import ogr, osr  # noqa
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class AreaParser(ABC):
    name: str
    url_code: str

    SRS_NAME: str = 'EPSG:4326'

    @abstractmethod
    def build_url(self, lat: float, lon: float) -> str:
        pass

    @abstractmethod
    def parse_gml_to_geojson(self, gml_content: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def parse_feature_properties_to_osm_tags(self, properties: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def replace_properties_with_osm_tags(self, geojson: Dict[str, Any]) -> None:
        for index, feature in enumerate(geojson['features']):
            properties = feature['properties']
            tags = self.parse_feature_properties_to_osm_tags(properties)
            geojson['features'][index]['properties'] = self.clean_empty_tags(tags)

    @staticmethod
    def clean_empty_tags(osm_tags: Dict[str, Any]) -> Dict[str, Any]:
        """
        Removes tags without values
        """
        return {k: v for k, v in osm_tags.items() if v is not None}


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


@dataclass(frozen=True)
class HealthCheckAreaReport:
    status_code: int
    is_building_data: bool = False
    is_expected_building_data: bool = False


@dataclass(frozen=True)
class HealthCheckReport:
    start_dt: str
    end_dt: str
    areas: Dict[str, HealthCheckAreaReport]
