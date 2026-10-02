from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_discover_endpoint():
    response = client.get("/discover")

    assert response.status_code == 200

    data = response.json()

    assert len(data["documented"]) == 5
    assert len(data["observed"]) == 7

    observed_status_codes = {
        (item["method"], item["path"]): item["status_code"]
        for item in data["observed"]
    }

    assert observed_status_codes[("GET", "/users")] == 200
    assert observed_status_codes[("POST", "/users")] == 201
    assert observed_status_codes[("GET", "/users/{id}")] == 200
    assert observed_status_codes[("DELETE", "/users/{id}")] == 204
    assert observed_status_codes[("POST", "/admin/users")] == 403

    shadow_paths = {
        (item["method"], item["path"])
        for item in data["shadow"]
    }

    zombie_paths = {
        (item["method"], item["path"])
        for item in data["zombie"]
    }

    assert ("POST", "/admin/users") in shadow_paths
    assert ("GET", "/internal/debug") in shadow_paths

    assert ("GET", "/old-users") in zombie_paths

    assert ("GET", "/users/{id}") not in shadow_paths


def test_traffic_to_discovery_integration():
    traffic_response = client.post(
        "/traffic",
        json={
            "method": "GET",
            "path": "/internal/test-endpoint",
            "status_code": 200,
        },
    )

    assert traffic_response.status_code == 200

    discovery_response = client.get("/discover")

    assert discovery_response.status_code == 200

    data = discovery_response.json()

    shadow_paths = {
        (item["method"], item["path"])
        for item in data["shadow"]
    }

    assert ("GET", "/internal/test-endpoint") in shadow_paths
