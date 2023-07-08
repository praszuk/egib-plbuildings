from os import path
from typing import Final

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: Final[str] = '/api/v1'
    PROJECT_NAME: Final[str] = 'egib-plbuildings'

    PROJECT_ROOT_DIR: Final[str] = path.realpath(
        path.join(path.dirname(__file__), '..', '..')
    )
    DATA_DIR: Final[str] = path.join(PROJECT_ROOT_DIR, 'data')
    POWIAT_DATA_FILENAME: Final[str] = path.join(DATA_DIR, 'powiats.geojson')
    POWIAT_GEOM_CACHE_FILENAME: Final[str] = '.powiat_geoms.pickle'


settings = Settings()
