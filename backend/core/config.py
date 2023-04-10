from typing import Final

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: Final = '/api/v1'
    PROJECT_NAME: Final = 'egib-plbuildings'


settings = Settings()
