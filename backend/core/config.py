from os import path
from typing import Final

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: Final[str] = '/api/v1'
    PROJECT_NAME: Final[str] = 'egib-plbuildings'

    PROJECT_ROOT_DIR: Final[str] = path.realpath(path.join(path.dirname(__file__), '..', '..'))
    APP_DIR: Final[str] = path.realpath(path.join(path.dirname(__file__), '..'))

    STATIC_DIR: Final[str] = path.join(APP_DIR, 'static')

    DATA_DIR: Final[str] = path.join(PROJECT_ROOT_DIR, 'data')
    CACHE_DIR: Final[str] = path.join(PROJECT_ROOT_DIR, '.cache')

    COUNTIES_DATA_FILENAME: Final[str] = path.join(CACHE_DIR, 'counties.geojson')
    COUNTIES_GEOM_CACHE_FILENAME: Final[str] = '.counties_geoms.pickle'
    COMMUNES_DATA_FILENAME: Final[str] = path.join(CACHE_DIR, 'communes.geojson')
    COMMUNES_GEOM_CACHE_FILENAME: Final[str] = '.communes_geoms.pickle'
    AREAS_HEALTHCHECK_CACHE_FILENAME: Final[str] = '.areas_healthcheck_result.json'


settings = Settings()
