from app.inventory import generate_inventory
from app.models import APIEndpoint


def test_inventory_classification():
    documented = [
        APIEndpoint(
            path="/users",
            method="GET",
            source="openapi"
        )
    ]

    observed = [
        APIEndpoint(
            path="/users",
            method="GET",
            source="traffic"
        ),
        APIEndpoint(
            path="/admin",
            method="GET",
            source="traffic"
        )
    ]

    inventory = generate_inventory(documented, observed)

    assert {
        "path": "/users",
        "method": "GET",
        "status": "DOCUMENTED"
    } in inventory

    assert {
        "path": "/admin",
        "method": "GET",
        "status": "SHADOW"
    } in inventory
