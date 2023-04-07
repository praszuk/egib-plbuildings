import pytest

from fastapi.testclient import TestClient

from os import path

from core.config import settings
from main import app


@pytest.fixture(scope='session')
def test_data_dir():
    return path.join(path.dirname(__file__), 'data')


@pytest.fixture(name='client', scope='session')
def test_client():
    client = TestClient(app)
    client.base_url = client.base_url.join(settings.API_V1_STR)
    yield client
