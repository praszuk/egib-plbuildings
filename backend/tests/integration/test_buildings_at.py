from os import path

import pytest

from backend.areas.finder import area_finder
from backend.services import buildings
from backend.models.building import Building


MOCK_AREA_TERYT_VALUE = '1421'


def test_invalid_lat_lon(client):
    response = client.get('buildings/', params={'lat': 91.0, 'lon': 50.0})
    assert response.status_code == 422

    response = client.get('buildings/', params={'lat': 90.0, 'lon': 181.0})
    assert response.status_code == 422

    response = client.get('buildings/', params={'lat': 91.0, 'lon': 181.0})
    assert response.status_code == 422


async def mock_download_gml(test_epodgik_data_dir, filename: str) -> str:
    """
    Override _download_gml from services buildings to return gml content
    from file
    :return: gml_content as string
    """
    filename = path.join(test_epodgik_data_dir, filename)
    with open(filename, 'r') as f:
        return f.read()


@pytest.mark.anyio
async def test_live_simple_building_data(async_client, monkeypatch, test_epodgik_data_dir):
    monkeypatch.setattr(
        buildings,
        '_download_gml',
        lambda client, url: mock_download_gml(test_epodgik_data_dir, 'gml_basic_building.xml'),
    )
    monkeypatch.setattr(area_finder, 'area_at', lambda lat, lon: MOCK_AREA_TERYT_VALUE)

    response = await async_client.get('buildings/', params={'lat': 50, 'lon': 20, 'live': True})

    assert response.status_code == 200
    data = response.json()

    assert len(data['features']) == 1
    tags = data['features'][0]['properties']
    assert 'building' in tags
    assert all(v is not None for v in tags.values())


@pytest.mark.anyio
async def test_live_multiple_buildings_data_returns_only_one(
    async_client, monkeypatch, test_epodgik_data_dir
):
    monkeypatch.setattr(
        buildings,
        '_download_gml',
        lambda client, url: mock_download_gml(test_epodgik_data_dir, 'gml_multiple_buildings.xml'),
    )
    monkeypatch.setattr(area_finder, 'area_at', lambda lat, lon: MOCK_AREA_TERYT_VALUE)

    response = await async_client.get('buildings/', params={'lat': 50, 'lon': 20, 'live': True})

    assert response.status_code == 200
    data = response.json()

    assert len(data['features']) == 1
    assert 'building' in data['features'][0]['properties']


@pytest.mark.anyio
async def test_live_no_building_data(async_client, monkeypatch, test_epodgik_data_dir):
    monkeypatch.setattr(
        buildings,
        '_download_gml',
        lambda client, url: mock_download_gml(test_epodgik_data_dir, 'gml_no_building.xml'),
    )
    monkeypatch.setattr(area_finder, 'area_at', lambda lat, lon: MOCK_AREA_TERYT_VALUE)

    response = await async_client.get('buildings/', params={'lat': 50, 'lon': 20, 'live': True})

    assert response.status_code == 200
    data = response.json()

    assert len(data['features']) == 0


@pytest.mark.anyio
async def test_db_simple_building_data(async_client, db):
    lat1, lon1 = 52.2299575, 21.0078368
    lat2, lon2 = 52.2300253, 21.0081468
    lat3, lon3 = 52.2301984, 21.0080464
    lat_search, lon_search = 52.2300062, 21.0079251

    wkt_polygon = f'POLYGON(({lon1} {lat1}, {lon2} {lat2}, {lon3} {lat3}, {lon1} {lat1}))'

    building = Building(
        geometry=wkt_polygon, tags={'building': 'house', 'building:levels': 2}, teryt='123456'
    )
    db.add(building)
    db.commit()
    db.refresh(building)

    response = await async_client.get(
        'buildings/', params={'lat': lat_search, 'lon': lon_search, 'live': False}
    )
    assert response.status_code == 200

    result = response.json()
    feature = result['features'][0]
    assert feature['geometry']['coordinates'][0][0] == [lon1, lat1]
    assert feature['properties'] == {'building': 'house', 'building:levels': 2}


@pytest.mark.anyio
async def test_db_multiple_building_data_returns_only_one(async_client, db):
    lat1, lon1 = 52.2299575, 21.0078368
    lat2, lon2 = 52.2300253, 21.0081468
    lat3, lon3 = 52.2301984, 21.0080464
    lat_search, lon_search = 52.2300062, 21.0079251

    wkt_polygon = f'POLYGON(({lon1} {lat1}, {lon2} {lat2}, {lon3} {lat3}, {lon1} {lat1}))'

    building1 = Building(
        geometry=wkt_polygon, tags={'building': 'house', 'building:levels': 2}, teryt='123456'
    )
    building2 = Building(
        geometry=wkt_polygon, tags={'building': 'yes', 'building:levels': 3}, teryt='123456'
    )
    db.add(building1)
    db.add(building2)
    db.commit()

    assert db.query(Building).count() == 2

    response = await async_client.get(
        'buildings/', params={'lat': lat_search, 'lon': lon_search, 'live': False}
    )
    assert response.status_code == 200

    result = response.json()
    assert len(result['features']) == 1


@pytest.mark.anyio
async def test_db_no_building_data(async_client, db):
    lat_search, lon_search = 52.2300062, 21.0079251

    assert db.query(Building).count() == 0

    response = await async_client.get(
        'buildings/', params={'lat': lat_search, 'lon': lon_search, 'live': False}
    )
    assert response.status_code == 200

    result = response.json()
    assert len(result['features']) == 0
