import json
import pickle
from typing import Any, Dict

from osgeo import ogr, osr  # noqa

from backend.core.config import settings
from backend.core.logger import logger
from backend.areas.models import AreaGeometry
from backend.exceptions import AreaDataNotFound, AreaNotFound

MAX_TILE_ZOOM = 11
TERYT_KEY = 'JPT_KOD_JE'


class AreaFinder:
    def __init__(self) -> None:
        self._county_geoms: Dict[str, AreaGeometry] = {}

    def load_data(self, counties_data_filename: str = settings.COUNTIES_DATA_FILENAME) -> None:
        logger.info('Loading areas geometries...')
        try:
            with open(settings.COUNTIES_GEOM_CACHE_FILENAME, 'rb') as f:
                self._county_geoms.update(pickle.load(f))
                logger.info('Completed loading areas geometries.')
                return
        except FileNotFoundError:
            logger.info('Cache file with areas geometries not found.')
        except (pickle.PickleError, TypeError, AttributeError):
            logger.exception('Cache file with areas geometries is damaged.')

        logger.info('Generating areas geometries using GeoJSON ' f'{counties_data_filename}')
        geojson = json.load(open(counties_data_filename, 'r'))
        self._county_geoms.update(self.parse_county_geojson_to_county_geoms(geojson))
        self.save_data()
        logger.info('Completed loading areas geometries.')

    def save_data(self) -> None:
        logger.info('Saving areas geometries to cache file.')
        try:
            with open(settings.COUNTIES_GEOM_CACHE_FILENAME, 'wb') as f:
                pickle.dump(self._county_geoms, f)
        except (IOError, pickle.PickleError):
            logger.exception('Error at serializing areas geometries to cache file.')

    def area_at(self, lat: float, lon: float) -> str:
        """
        :param lat: latitude
        :param lon: longitude
        :return: teryt id where lat/lon is within
        :raises AreaDataNotFound – if area data is not loaded,
        AreaNotFound if not found area for given coordinates
        """
        if not self._county_geoms:
            raise AreaDataNotFound()

        pt = ogr.Geometry(ogr.wkbPoint)
        sr = osr.SpatialReference()
        sr.SetWellKnownGeogCS('WGS84')
        pt.AssignSpatialReference(sr)
        pt.SetPoint_2D(0, lon, lat)

        for teryt, county_geom in self._county_geoms.items():
            if pt.Within(county_geom.geom):
                return teryt

        raise AreaNotFound(f'Not found area at: {lat} {lon}')

    @staticmethod
    def parse_area_geojson_to_area_geoms(
        geojson: Dict[str, Any], teryt_key: str = TERYT_KEY
    ) -> Dict[str, AreaGeometry]:
        """
        :param geojson: features where each one is different areas
        cooridnates should be in WGS84 projection (EPSG:4326)
        :param teryt_key: key name in feature properties which contains unique
        teryt value for area.
        :return: dict where key is area id (teryt)
        and value is parsed as AreaGeometry (with GDAL ogr Geometry)
        """
        areas = {}
        for feature in geojson['features']:
            teryt = feature['properties'][teryt_key]
            geometry: ogr.Geometry = ogr.CreateGeometryFromJson(json.dumps(feature['geometry']))
            areas[teryt] = AreaGeometry(geometry)

        return areas


area_finder = AreaFinder()
