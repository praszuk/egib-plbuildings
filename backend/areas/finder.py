import json
import pickle
from typing import Any, Dict, List

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
        self._commune_geoms: Dict[str, AreaGeometry] = {}
        self._county_communes: Dict[str, List[str]] = {}

    def load_data(self) -> None:
        def _load(area_type, cache_file, data_file):
            logger.info(f'Loading {area_type} geometries...')
            try:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            except FileNotFoundError:
                logger.info(f'Cache file with {area_type} geometries not found.')
            except (pickle.PickleError, ModuleNotFoundError, TypeError, AttributeError):
                logger.exception(f'Cache file with {area_type} geometries is damaged.')

            logger.info(f'Generating {area_type} geometries using GeoJSON {data_file}')
            geojson = json.load(open(data_file, 'r'))
            return self.parse_area_geojson_to_area_geoms(geojson)

        self._county_geoms.update(
            _load(
                'counties', settings.COUNTIES_GEOM_CACHE_FILENAME, settings.COUNTIES_DATA_FILENAME
            )
        )
        self._commune_geoms.update(
            _load(
                'communes', settings.COMMUNES_GEOM_CACHE_FILENAME, settings.COMMUNES_DATA_FILENAME
            )
        )
        self.save_data()
        self.generate_county_communes()
        logger.info(f'Completed loading {len(self._county_geoms)} counties geometries.')
        logger.info(f'Completed loading {len(self._commune_geoms)} communes geometries.')

    def generate_county_communes(self):
        for commune_teryt in self._commune_geoms.keys():
            county_teryt = commune_teryt[:4]
            if county_teryt not in self._county_communes:
                self._county_communes[county_teryt] = []

            self._county_communes[county_teryt].append(commune_teryt)

    def save_data(self) -> None:
        logger.info('Saving areas geometries to cache file.')
        try:
            with open(settings.COUNTIES_GEOM_CACHE_FILENAME, 'wb') as f:
                pickle.dump(self._county_geoms, f)
            with open(settings.COMMUNES_GEOM_CACHE_FILENAME, 'wb') as f:
                pickle.dump(self._commune_geoms, f)
        except (IOError, pickle.PickleError):
            logger.exception('Error at serializing areas geometries to cache file.')

    def area_at(self, lat: float, lon: float) -> str:
        """
        :param lat: latitude
        :param lon: longitude
        :return: teryt id where lat/lon is within, it can be county or commune value
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

        county_teryt = None
        for teryt, county_geom in self._county_geoms.items():
            if pt.Within(county_geom.geom):
                county_teryt = teryt
                break

        if county_teryt is not None and county_teryt not in self._county_communes:
            return county_teryt

        elif county_teryt in self._county_communes:
            # point might be in a commune which is also in a county
            for commune_teryt in self._county_communes.get(county_teryt):
                if pt.Within(self._commune_geoms[commune_teryt].geom):
                    return commune_teryt

            return county_teryt

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
