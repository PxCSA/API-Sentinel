import yaml
from pathlib import Path

from .models import APIEndpoint


def parse_openapi(file_path: str) -> list[APIEndpoint]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        spec = yaml.safe_load(file)

    endpoints = []

    for endpoint_path, methods in spec.get("paths", {}).items():
        for method, details in methods.items():

            if method.lower() not in {
                "get",
                "post",
                "put",
                "patch",
                "delete",
                "options",
                "head",
            }:
                continue

            endpoints.append(
              APIEndpoint(
                 path=endpoint_path,
                 method=method.upper(),
                 source="openapi",
                 description=(
                     details.get("summary")
                     or details.get("description")
         ),
      deprecated=details.get("deprecated", False),
) 
            )

    return endpoints