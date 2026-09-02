from .models import APIEndpoint, ShadowAPI, APIInventoryItem
from .endpoint_normalizer import normalize_endpoint


def find_shadow_apis(
    documented: list[APIEndpoint],
    observed: list[APIEndpoint],
) -> list[ShadowAPI]:
    """
    Compare documented APIs with observed traffic
    and identify undocumented Shadow APIs.
    """

    documented_set = {
        (endpoint.method.upper(), normalize_endpoint(endpoint.path))
        for endpoint in documented
    }

    shadow_apis = []

    for endpoint in observed:
        normalized_path = normalize_endpoint(endpoint.path)
        key = (endpoint.method.upper(), normalized_path)

        if key not in documented_set:

            if (
                normalized_path.startswith("/admin")
                or normalized_path.startswith("/internal")
                or endpoint.method.upper() in {"POST", "PUT", "PATCH", "DELETE"}
            ):
                risk = "HIGH"
                reason = "Endpoint appears to expose an administrative, internal, or modifying resource."
            else:
                risk = "MEDIUM"
                reason = "Undocumented API endpoint."

            shadow_apis.append(
                ShadowAPI(
                    path=normalized_path,
                    method=endpoint.method.upper(),
                    source="traffic",
                    description="Undocumented API endpoint",
                    risk=risk,
                    reason=reason,
                )
            )

    return shadow_apis


def build_inventory(
    documented: list[APIEndpoint],
    observed: list[APIEndpoint],
    shadow: list[ShadowAPI],
) -> list[APIInventoryItem]:
    """
    Build complete API inventory and classify endpoints.
    """

    inventory = []

    # Documented APIs
    for endpoint in documented:
        inventory.append(
            APIInventoryItem(
                path=endpoint.path,
                method=endpoint.method.upper(),
                status="DOCUMENTED",
                source="openapi",
                description=endpoint.description,
            )
        )

    # Shadow APIs
    for endpoint in shadow:
        inventory.append(
            APIInventoryItem(
                path=endpoint.path,
                method=endpoint.method.upper(),
                status="SHADOW",
                source="traffic",
                description=endpoint.description,
                risk=endpoint.risk,
                reason=endpoint.reason,
            )
        )

    return inventory