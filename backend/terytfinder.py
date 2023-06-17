import json
from typing import Any, Dict

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
