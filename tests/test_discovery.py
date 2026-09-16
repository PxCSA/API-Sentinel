from app.discovery_engine import find_shadow_apis, find_zombie_apis
from app.models import APIEndpoint


def test_shadow_api_detection():
    documented = [
        APIEndpoint(
            path="/users",
            method="GET",
            source="openapi",
        ),
        APIEndpoint(
            path="/users",
            method="POST",
            source="openapi",
        ),
        APIEndpoint(
            path="/users/{id}",
            method="GET",
            source="openapi",
        ),
        APIEndpoint(
            path="/users/{id}",
            method="DELETE",
            source="openapi",
        ),
    ]

    observed = [
        APIEndpoint(
            path="/users",
            method="GET",
            source="traffic",
        ),
        APIEndpoint(
            path="/users/101",
            method="GET",
            source="traffic",
        ),
        APIEndpoint(
            path="/admin/users",
            method="POST",
            source="traffic",
        ),
        APIEndpoint(
            path="/internal/debug",
            method="GET",
            source="traffic",
        ),
    ]

    shadow = find_shadow_apis(documented, observed)

    shadow_paths = {
        (endpoint.method, endpoint.path)
        for endpoint in shadow
    }

    assert ("POST", "/admin/users") in shadow_paths
    assert ("GET", "/internal/debug") in shadow_paths

    # /users/101 should match documented /users/{id}
    assert ("GET", "/users/{id}") not in shadow_paths


def test_zombie_api_detection():
    documented = [
        APIEndpoint(
            path="/users",
            method="GET",
            source="openapi",
        ),
        APIEndpoint(
            path="/old-users",
            method="GET",
            source="openapi",
            deprecated=True,
        ),
    ]

    observed = [
        APIEndpoint(
            path="/users",
            method="GET",
            source="traffic",
        ),
        APIEndpoint(
            path="/old-users",
            method="GET",
            source="traffic",
        ),
    ]

    zombie = find_zombie_apis(documented, observed)

    zombie_paths = {
        (endpoint.method, endpoint.path)
        for endpoint in zombie
    }

    assert ("GET", "/old-users") in zombie_paths


def test_deprecated_api_not_used_is_not_zombie():
    documented = [
        APIEndpoint(
            path="/old-users",
            method="GET",
            source="openapi",
            deprecated=True,
        ),
    ]

    observed = []

    zombie = find_zombie_apis(documented, observed)

    assert len(zombie) == 0