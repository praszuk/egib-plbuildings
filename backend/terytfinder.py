import json
from typing import Any, Dict, Optional

from osgeo import ogr, osr  # noqa

from .core.config import settings

MAX_TILE_ZOOM = 11
TERYT_KEY = 'JPT_KOD_JE'


class PowiatFinder:
    def __init__(self):
        self._powiats_geom = {}

    def load_data(self, powiat_data_filename=settings.POWIAT_DATA_FILENAME):
        geojson = json.load(open(powiat_data_filename, 'r'))
        self._powiats_geom = self.parse_powiat_geojson_to_ogr_geom(geojson)

    def powiat_at(self, lat, lon) -> Optional[str]:
        """
        :param lat: latitude
        :param lon: longitude
        :return: teryt id where lat/lon is within or return None if not found
        """
        if not self._powiats_geom:
            return None

        pt = ogr.Geometry(ogr.wkbPoint)
        sr = osr.SpatialReference()
        sr.SetWellKnownGeogCS('WGS84')
        pt.AssignSpatialReference(sr)
        pt.SetPoint_2D(0, lon, lat)

        for teryt, geom in self._powiats_geom.items():
            if pt.Within(geom):
                return teryt

        return None

    @staticmethod
    def parse_powiat_geojson_to_ogr_geom(
        geojson: Dict[str, Any], teryt_key: str = TERYT_KEY
    ) -> Dict[str, ogr.Geometry]:
        """
        :param geojson: features where each one is different powiat
        cooridnates should be in WGS84 projection (EPSG:4326)
        :param teryt_key: key name in feature properties which contains unique
        teryt value for powiat.
        :return: dict where key is powiat id (teryt)
        and value is parsed GDAL ogr Geometry
        """
        powiats = {}
        for feature in geojson['features']:
            teryt = feature['properties'][teryt_key]
            geometry: ogr.Geometry = ogr.CreateGeometryFromJson(
                json.dumps(feature['geometry'])
            )
            powiats[teryt] = geometry

        return powiats
