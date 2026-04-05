def test_index_get(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Choose a city" in rv.data


def test_index_post_mumbai(client):
    rv = client.post("/", data={"city": "mumbai"})
    assert rv.status_code == 200
    assert b"Mumbai" in rv.data
    assert b"\xc2\xb0C" in rv.data or b"C" in rv.data


def test_index_post_invalid_city(client):
    rv = client.post("/", data={"city": "not-a-city"})
    assert rv.status_code == 200
    assert b"Invalid city" in rv.data
