import pytest

from os import path


@pytest.fixture(scope='session')
def test_data_dir():
    return path.join(path.dirname(__file__), 'data')
