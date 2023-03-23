from pydantic import BaseSettings

from typing import Final


class Settings(BaseSettings):
    API_V1_STR: Final = '/api/v1'
    PROJECT_NAME: Final = 'egib-plbuildings'


settings = Settings()
