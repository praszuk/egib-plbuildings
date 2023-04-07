def test_invalid_lat_lon(client):
    response = client.get('buildings/', params={'lat': 91.0, 'lon': 50.0})
    assert response.status_code == 422

    response = client.get('buildings/', params={'lat': 90.0, 'lon': 181.0})
    assert response.status_code == 422

    response = client.get('buildings/', params={'lat': 91.0, 'lon': 181.0})
    assert response.status_code == 422

