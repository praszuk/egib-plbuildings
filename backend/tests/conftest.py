from os import path

import httpx
import pytest
from fastapi.testclient import TestClient

from backend.core.config import settings
from backend.main import app


@pytest.fixture
def anyio_backend():  # without it tests are executed twice
    return 'trio'


@pytest.fixture(scope='session')
def test_epodgik_data_dir():
    return path.join(path.dirname(__file__), 'data', 'epodgik')


@pytest.fixture(scope='session')
def test_geoportal2_data_dir():
    return path.join(path.dirname(__file__), 'data', 'geoportal2')


@pytest.fixture(scope='session')
def test_geoportal_data_dir():
    return path.join(path.dirname(__file__), 'data', 'geoportal')


@pytest.fixture(scope='session')
def project_data_dir():
    return settings.DATA_DIR


@pytest.fixture(name='client', scope='session')
def test_client():
    client = TestClient(app)
    client.base_url = client.base_url.join(settings.API_V1_STR)
    yield client


@pytest.fixture(name='async_client')
async def test_async_client():
    async with httpx.AsyncClient(app=app, base_url='http://test') as client:
        client.base_url = client.base_url.join(settings.API_V1_STR)
        yield client


@pytest.fixture(scope='session')
def load_epodgik_gml(test_epodgik_data_dir):
    def inner(filename: str) -> str:
        with open(path.join(test_epodgik_data_dir, filename), 'r') as f:
            return f.read()

    return inner


@pytest.fixture(scope='session')
def load_geoportal2_gml(test_geoportal2_data_dir):
    def inner(filename: str) -> str:
        with open(path.join(test_geoportal2_data_dir, filename), 'r') as f:
            return f.read()

    return inner


@pytest.fixture(scope='session')
def load_geoportal_gml(test_geoportal_data_dir):
    def inner(filename: str) -> str:
        with open(path.join(test_geoportal_data_dir, filename), 'r') as f:
            return f.read()

    return inner
