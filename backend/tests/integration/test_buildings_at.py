from os import path

import pytest

from backend.services import buildings


def test_invalid_lat_lon(client):
    response = client.get('buildings/', params={'lat': 91.0, 'lon': 50.0})
    assert response.status_code == 422

    response = client.get('buildings/', params={'lat': 90.0, 'lon': 181.0})
    assert response.status_code == 422

    response = client.get('buildings/', params={'lat': 91.0, 'lon': 181.0})
    assert response.status_code == 422


async def mock_download_gml(test_data_dir, filename: str) -> str:
    """
    Override _download_gml from services buildings to return gml content
    from file
    :return: gml_content as string
    """
    filename = path.join(test_data_dir, filename)
    with open(filename, 'r') as f:
        return f.read()


@pytest.mark.anyio
async def test_simple_building_data(async_client, monkeypatch, test_data_dir):
    monkeypatch.setattr(
        buildings,
        '_download_gml',
        lambda client, url: mock_download_gml(
            test_data_dir, 'gml_basic_building.xml'
        ),
    )

    response = await async_client.get(
        'buildings/', params={'lat': 50, 'lon': 20}
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data['features']) == 1
    assert 'building' in data['features'][0]['properties']


@pytest.mark.anyio
async def test_multiple_buildings_data_returns_only_one(
    async_client, monkeypatch, test_data_dir
):
    monkeypatch.setattr(
        buildings,
        '_download_gml',
        lambda client, url: mock_download_gml(
            test_data_dir, 'gml_multiple_buildings.xml'
        ),
    )

    response = await async_client.get(
        'buildings/', params={'lat': 50, 'lon': 20}
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data['features']) == 1
    assert 'building' in data['features'][0]['properties']


@pytest.mark.anyio
async def test_no_building_data(async_client, monkeypatch, test_data_dir):
    monkeypatch.setattr(
        buildings,
        '_download_gml',
        lambda client, url: mock_download_gml(
            test_data_dir, 'gml_no_building.xml'
        ),
    )

    response = await async_client.get(
        'buildings/', params={'lat': 50, 'lon': 20}
    )

    assert response.status_code == 200
    data = response.json()

    assert len(data['features']) == 0
