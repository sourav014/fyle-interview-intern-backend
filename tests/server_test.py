def test_server_health(client):
    response = client.get(
        '/'
    )

    assert response.status_code == 200

    res = response.json
    assert res['status'] == 'ready'