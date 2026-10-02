import json
from pathlib import Path

from .models import APIEndpoint
from .endpoint_normalizer import normalize_endpoint


def parse_traffic(file_path: str) -> list[APIEndpoint]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        traffic_data = json.load(file)

    observed = []

    for index, item in enumerate(traffic_data):
        method = item.get("method")
        endpoint_path = item.get("path")
        status_code = item.get("status_code")

        if not method:
            raise ValueError(
                f"Traffic record {index} is missing 'method'"
            )

        if not endpoint_path:
            raise ValueError(
                f"Traffic record {index} is missing 'path'"
            )

        endpoint = APIEndpoint(
            path=endpoint_path.strip(),
            method=method.strip().upper(),
            source="traffic",
            status_code=status_code,
        )

        observed.append(endpoint)

    return observed


def deduplicate_traffic(
    observed: list[APIEndpoint],
) -> list[APIEndpoint]:
    unique_endpoints = []
    seen = set()

    for endpoint in observed:
        normalized_path = normalize_endpoint(endpoint.path)
        key = (endpoint.method.upper(), normalized_path)

        if key not in seen:
            seen.add(key)

            unique_endpoints.append(
                APIEndpoint(
                    path=normalized_path,
                    method=endpoint.method.upper(),
                    source=endpoint.source,
                    description=endpoint.description,
                    deprecated=endpoint.deprecated,
                    status_code=endpoint.status_code,
                )
            )

    return unique_endpoints


def parse_traffic_records(records: list[dict]) -> list[APIEndpoint]:
    observed = []

    for index, item in enumerate(records):
        method = item.get("method")
        endpoint_path = item.get("path")
        status_code = item.get("status_code")

        if not method:
            raise ValueError(
                f"Traffic record {index} is missing 'method'"
            )

        if not endpoint_path:
            raise ValueError(
                f"Traffic record {index} is missing 'path'"
            )

        endpoint = APIEndpoint(
            path=endpoint_path.strip(),
            method=method.strip().upper(),
            source="traffic",
            status_code=status_code,
        )

        observed.append(endpoint)

    return observed
