import pytest

from fastapi.testclient import TestClient

from os import path

from core.config import settings
from main import app


@pytest.fixture
def anyio_backend():  # without it tests are executed twice
    return 'trio'


@pytest.fixture(scope='session')
def test_data_dir():
    return path.join(path.dirname(__file__), 'data')


@pytest.fixture(name='client', scope='session')
def test_client():
    client = TestClient(app)
    client.base_url = client.base_url.join(settings.API_V1_STR)
    yield client


@pytest.fixture(scope='session')
def load_gml(test_data_dir):
    def inner(filename: str) -> str:
        with open(path.join(test_data_dir, filename), 'r') as f:
            return f.read()

    return inner
