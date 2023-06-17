from os import path
from typing import Final

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: Final = '/api/v1'
    PROJECT_NAME: Final = 'egib-plbuildings'

    PROJECT_ROOT_DIR: str = path.realpath(
        path.join(path.dirname(__file__), '..', '..')
    )
    DATA_DIR: Final = path.join(PROJECT_ROOT_DIR, 'data')
    POWIAT_DATA_FILENAME: Final = path.join(DATA_DIR, 'powiats.geojson')


settings = Settings()
