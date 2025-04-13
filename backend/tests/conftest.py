import httpx
import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from os import path, environ
from unittest.mock import patch

from backend.core.config import settings
from backend.database.base import Base
from backend.database.session import get_db
from backend.main import app


TEST_DB_NAME = 'test_db'
TEST_DB_URL = 'postgresql://{}:{}@{}/{}'.format(
    environ.get('POSTGRES_USER'),
    environ.get('POSTGRES_PASSWORD'),
    environ.get('POSTGRES_HOST'),
    TEST_DB_NAME,
)

transport = ASGITransport(app=app)


def create_db():
    engine = create_engine(settings.DATABASE_URL)
    conn = engine.connect()
    conn.execute(text('COMMIT'))
    try:
        conn.execute(
            text(f"CREATE DATABASE {TEST_DB_NAME} WITH OWNER '{environ.get('POSTGRES_USER')}'")
        )
    except Exception as e:
        if 'already exists' not in str(e):
            raise
    conn.close()


def drop_db():
    engine = create_engine(settings.DATABASE_URL)
    conn = engine.connect()
    conn.execute(text('COMMIT'))
    conn.execute(text(f'DROP DATABASE IF EXISTS {TEST_DB_NAME}'))
    conn.close()


@pytest.fixture(scope='session')
def setup_db():
    create_db()

    engine = create_engine(TEST_DB_URL)
    conn = engine.connect()
    conn.execute(text('CREATE EXTENSION IF NOT EXISTS postgis'))
    conn.commit()
    conn.close()

    yield

    engine.dispose()
    drop_db()


@pytest.fixture(scope='function')
def db(setup_db):
    engine = create_engine(TEST_DB_URL)

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # noqa
    db_session = Session()

    def override_get_db():
        yield db_session

    # patching here, because import task use external process
    # it doesn't have access to app overridden instance, so it won't work
    with patch('backend.tasks.import_buildings.get_db', side_effect=lambda: override_get_db()):
        try:
            app.dependency_overrides[get_db] = override_get_db
            yield db_session

        finally:
            db_session.close()
            Base.metadata.drop_all(bind=engine)
            engine.dispose()


@pytest.fixture
def anyio_backend():  # without it tests are executed twice
    return 'trio'


@pytest.fixture(scope='session')
def test_data_dir():
    return path.join(path.dirname(__file__), 'data')


@pytest.fixture(scope='session')
def load_gml(test_data_dir):
    def inner(subdir: str, filename: str) -> str:
        with open(path.join(test_data_dir, subdir, filename), 'r') as f:
            return f.read()

    return inner


@pytest.fixture(scope='session')
def project_data_dir():
    return settings.DATA_DIR


@pytest.fixture(name='client')
def test_client(db):
    client = TestClient(app)
    client.base_url = client.base_url.join(settings.API_V1_STR)
    yield client


@pytest.fixture(name='async_client')
async def test_async_client(db):
    async with httpx.AsyncClient(transport=transport, base_url='http://test') as client:
        client.base_url = client.base_url.join(settings.API_V1_STR)
        yield client


@pytest.fixture(scope='session')
def area_finder():
    from backend.areas.finder import area_finder as area_finder_instance

    area_finder_instance.load_data()

    return area_finder_instance
