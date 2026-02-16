def test_healthcheck(client):
    response = client.get("/heathcheck")
    assert response.status_code == 200
    assert response.json() == "OK"
