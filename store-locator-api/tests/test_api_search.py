from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_pagination_shape():
    payload = {
    "lat": 42.3555,
    "lon": -71.0602,
    "radius_miles": 50,
    "limit": 5,
    "offset": 0
}
    r = client.post("/api/stores/search", json=payload)
    print(r.status_code, r.json())
    assert r.status_code == 200

    data = r.json()
    assert "total" in data
    assert data["limit"] == 5
    assert data["offset"] == 0
    assert isinstance(data["results"], list)
    assert len(data["results"]) <= 5