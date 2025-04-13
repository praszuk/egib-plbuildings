from os import path, environ

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = 'egib-plbuildings'
    DATABASE_URL: str = 'postgresql://{}:{}@{}/{}'.format(
        environ.get('POSTGRES_USER'),
        environ.get('POSTGRES_PASSWORD'),
        environ.get('POSTGRES_HOST'),
        environ.get('POSTGRES_DB'),
    )

    PROJECT_ROOT_DIR: str = path.realpath(path.join(path.dirname(__file__), '..', '..'))
    APP_DIR: str = path.realpath(path.join(path.dirname(__file__), '..'))

    TEMPLATES_DIR: str = path.join(APP_DIR, 'templates')
    STATIC_DIR: str = path.join(APP_DIR, 'static')

    DATA_DIR: str = path.join(PROJECT_ROOT_DIR, 'data')
    CACHE_DIR: str = path.join(PROJECT_ROOT_DIR, '.cache')

    COUNTIES_DATA_FILENAME: str = path.join(DATA_DIR, 'counties.geojson')
    COUNTIES_GEOM_CACHE_FILENAME: str = path.join(CACHE_DIR, '.counties_geoms.pickle')
    COMMUNES_DATA_FILENAME: str = path.join(DATA_DIR, 'communes.geojson')
    COMMUNES_GEOM_CACHE_FILENAME: str = path.join(CACHE_DIR, '.communes_geoms.pickle')

    ACCESS_LOGGER: str = 'egib_access'
    DEFAULT_LOGGER: str = 'egib_default'


settings = Settings()
