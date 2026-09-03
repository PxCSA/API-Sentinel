from .models import APIEndpoint
from .endpoint_normalizer import normalize_endpoint


def generate_inventory(
    documented: list[APIEndpoint],
    observed: list[APIEndpoint],
):
    documented_set = {
        (
            endpoint.method.upper(),
            normalize_endpoint(endpoint.path)
        )
        for endpoint in documented
    }

    observed_set = {
        (
            endpoint.method.upper(),
            normalize_endpoint(endpoint.path)
        )
        for endpoint in observed
    }

    inventory = []

    # Documented APIs
    for method, path in documented_set:

        inventory.append({
            "path": path,
            "method": method,
            "status": "DOCUMENTED"
        })

    # Shadow APIs
    for method, path in observed_set:

        if (method, path) not in documented_set:

            inventory.append({
                "path": path,
                "method": method,
                "status": "SHADOW"
            })

    return inventory