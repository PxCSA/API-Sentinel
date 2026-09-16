from .models import APIEndpoint, ShadowAPI, ZombieAPI, APIInventoryItem
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
                reason = (
                    "Endpoint appears to expose an administrative, "
                    "internal, or modifying resource."
                )
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


def find_zombie_apis(
    documented: list[APIEndpoint],
    observed: list[APIEndpoint],
) -> list[ZombieAPI]:
    """
    Identify documented APIs that are marked as deprecated
    but are still being used in observed traffic.
    """

    deprecated_apis = {
        (
            endpoint.method.upper(),
            normalize_endpoint(endpoint.path),
        ): endpoint
        for endpoint in documented
        if endpoint.deprecated
    }

    zombie_apis = []

    for endpoint in observed:
        normalized_path = normalize_endpoint(endpoint.path)
        key = (endpoint.method.upper(), normalized_path)

        if key in deprecated_apis:
            documented_endpoint = deprecated_apis[key]

            zombie_apis.append(
                ZombieAPI(
                    path=normalized_path,
                    method=endpoint.method.upper(),
                    source="traffic",
                    description=(
                        documented_endpoint.description
                        or "Deprecated API endpoint"
                    ),
                    risk="MEDIUM",
                    reason="Deprecated API endpoint is still being used.",
                    deprecated=True,
                )
            )

    return zombie_apis


def build_inventory(
    documented: list[APIEndpoint],
    observed: list[APIEndpoint],
    shadow: list[ShadowAPI],
    zombie: list[ZombieAPI],
) -> list[APIInventoryItem]:
    """
    Build complete API inventory and classify endpoints.
    """

    inventory = []

    documented_keys = {
        (
            endpoint.method.upper(),
            normalize_endpoint(endpoint.path),
        )
        for endpoint in documented
    }

    shadow_keys = {
        (
            endpoint.method.upper(),
            normalize_endpoint(endpoint.path),
        )
        for endpoint in shadow
    }

    zombie_keys = {
        (
            endpoint.method.upper(),
            normalize_endpoint(endpoint.path),
        )
        for endpoint in zombie
    }

    observed_keys = {
        (
            endpoint.method.upper(),
            normalize_endpoint(endpoint.path),
        )
        for endpoint in observed
    }

    # Documented APIs
    for endpoint in documented:

        key = (
            endpoint.method.upper(),
            normalize_endpoint(endpoint.path),
        )

        if endpoint.deprecated:
            status = "DEPRECATED"
        elif key in observed_keys:
            status = "ACTIVE"
        else:
            status = "DOCUMENTED"

        inventory.append(
            APIInventoryItem(
                path=endpoint.path,
                method=endpoint.method.upper(),
                status=status,
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

    # Zombie APIs
    for endpoint in zombie:

        inventory.append(
            APIInventoryItem(
                path=endpoint.path,
                method=endpoint.method.upper(),
                status="ZOMBIE",
                source="traffic",
                description=endpoint.description,
                risk=endpoint.risk,
                reason=endpoint.reason,
            )
        )

    return inventory