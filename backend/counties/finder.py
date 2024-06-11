import json
import pickle
from typing import Any, Dict

from osgeo import ogr, osr  # noqa

from backend.core.config import settings
from backend.core.logger import logger
from backend.counties.models import CountyGeometry
from backend.exceptions import CountyDataNotFound, CountyNotFound

MAX_TILE_ZOOM = 11
TERYT_KEY = 'JPT_KOD_JE'


class CountyFinder:
    def __init__(self) -> None:
        self._county_geoms: Dict[str, CountyGeometry] = {}

    def load_data(
        self, counties_data_filename: str = settings.COUNTIES_DATA_FILENAME
    ) -> None:
        logger.info('Loading counties geometries...')
        try:
            with open(settings.COUNTIES_GEOM_CACHE_FILENAME, 'rb') as f:
                self._county_geoms.update(pickle.load(f))
                logger.info('Completed loading counties geometries.')
                return
        except FileNotFoundError:
            logger.info('Cache file with counties geometries not found.')
        except (pickle.PickleError, TypeError, AttributeError):
            logger.exception('Cache file with counties geometries is damaged.')

        logger.info(
            'Generating counties geometries using GeoJSON '
            f'{counties_data_filename}'
        )
        geojson = json.load(open(counties_data_filename, 'r'))
        self._county_geoms.update(
            self.parse_county_geojson_to_county_geoms(geojson)
        )
        self.save_data()
        logger.info('Completed loading counties geometries.')

    def save_data(self) -> None:
        logger.info('Saving counties geometries to cache file.')
        try:
            with open(settings.COUNTIES_GEOM_CACHE_FILENAME, 'wb') as f:
                pickle.dump(self._county_geoms, f)
        except (IOError, pickle.PickleError):
            logger.exception(
                'Error at serializing counties geometries to cache file.'
            )

    def county_at(self, lat: float, lon: float) -> str:
        """
        :param lat: latitude
        :param lon: longitude
        :return: teryt id where lat/lon is within
        :raises CountyDataNotFound – if county data is not loaded,
        CountyNotFound if not found county for given coordinates
        """
        if not self._county_geoms:
            raise CountyDataNotFound()

        pt = ogr.Geometry(ogr.wkbPoint)
        sr = osr.SpatialReference()
        sr.SetWellKnownGeogCS('WGS84')
        pt.AssignSpatialReference(sr)
        pt.SetPoint_2D(0, lon, lat)

        for teryt, county_geom in self._county_geoms.items():
            if pt.Within(county_geom.geom):
                return teryt

        raise CountyNotFound(f'Not found county at: {lat} {lon}')

    @staticmethod
    def parse_county_geojson_to_county_geoms(
        geojson: Dict[str, Any], teryt_key: str = TERYT_KEY
    ) -> Dict[str, CountyGeometry]:
        """
        :param geojson: features where each one is different counties
        cooridnates should be in WGS84 projection (EPSG:4326)
        :param teryt_key: key name in feature properties which contains unique
        teryt value for county.
        :return: dict where key is county id (teryt)
        and value is parsed as CountyGeometry (with GDAL ogr Geometry)
        """
        counties = {}
        for feature in geojson['features']:
            teryt = feature['properties'][teryt_key]
            geometry: ogr.Geometry = ogr.CreateGeometryFromJson(
                json.dumps(feature['geometry'])
            )
            counties[teryt] = CountyGeometry(geometry)

        return counties


county_finder = CountyFinder()
