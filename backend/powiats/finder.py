import json
import pickle
from typing import Any, Dict

from osgeo import ogr, osr  # noqa

from backend.core.config import settings
from backend.core.logger import logger
from backend.exceptions import PowiatDataNotFound, PowiatNotFound
from backend.powiats.models import PowiatGeometry

MAX_TILE_ZOOM = 11
TERYT_KEY = 'JPT_KOD_JE'


class PowiatFinder:
    def __init__(self) -> None:
        self._powiat_geoms: Dict[str, PowiatGeometry] = {}

    def load_data(
        self, powiat_data_filename: str = settings.POWIAT_DATA_FILENAME
    ) -> None:
        logger.info('Loading powiat geometries...')
        try:
            with open(settings.POWIAT_GEOM_CACHE_FILENAME, 'rb') as f:
                self._powiat_geoms.update(pickle.load(f))
                logger.info('Completed loading powiat geometries.')
                return
        except FileNotFoundError:
            logger.info('Cache file with powiat geometries not found.')
        except (pickle.PickleError, TypeError, AttributeError):
            logger.exception('Cache file with powiat geometries is damaged.')

        logger.info(
            'Generating powiat geometries using GeoJSON '
            f'{powiat_data_filename}'
        )
        geojson = json.load(open(powiat_data_filename, 'r'))
        self._powiat_geoms.update(
            self.parse_powiat_geojson_to_powiat_geoms(geojson)
        )
        self.save_data()
        logger.info('Completed loading powiat geometries.')

    def save_data(self) -> None:
        logger.info('Saving powiat geometries to cache file.')
        try:
            with open(settings.POWIAT_GEOM_CACHE_FILENAME, 'wb') as f:
                pickle.dump(self._powiat_geoms, f)
        except (IOError, pickle.PickleError):
            logger.exception(
                'Error at serializing powiat geometries to cache file.'
            )

    def powiat_at(self, lat: float, lon: float) -> str:
        """
        :param lat: latitude
        :param lon: longitude
        :return: teryt id where lat/lon is within
        :raises PowiatDataNotFound – if powiat data is not loaded,
        PowiatNotFound if not found powiat for given coordinates
        """
        if not self._powiat_geoms:
            raise PowiatDataNotFound()

        pt = ogr.Geometry(ogr.wkbPoint)
        sr = osr.SpatialReference()
        sr.SetWellKnownGeogCS('WGS84')
        pt.AssignSpatialReference(sr)
        pt.SetPoint_2D(0, lon, lat)

        for teryt, powiat_geom in self._powiat_geoms.items():
            if pt.Within(powiat_geom.geom):
                return teryt

        raise PowiatNotFound(f'Not found powiat at: {lat} {lon}')

    @staticmethod
    def parse_powiat_geojson_to_powiat_geoms(
        geojson: Dict[str, Any], teryt_key: str = TERYT_KEY
    ) -> Dict[str, PowiatGeometry]:
        """
        :param geojson: features where each one is different powiat
        cooridnates should be in WGS84 projection (EPSG:4326)
        :param teryt_key: key name in feature properties which contains unique
        teryt value for powiat.
        :return: dict where key is powiat id (teryt)
        and value is parsed as PowiatGeometry (with GDAL ogr Geometry)
        """
        powiats = {}
        for feature in geojson['features']:
            teryt = feature['properties'][teryt_key]
            geometry: ogr.Geometry = ogr.CreateGeometryFromJson(
                json.dumps(feature['geometry'])
            )
            powiats[teryt] = PowiatGeometry(geometry)

        return powiats


powiat_finder = PowiatFinder()
