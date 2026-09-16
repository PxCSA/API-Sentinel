import json
from pathlib import Path

from fastapi import FastAPI

from .discovery_engine import (
    find_shadow_apis,
    find_zombie_apis,
    build_inventory,
)
from .models import APIEndpoint, DiscoveryResult
from .openapi_parser import parse_openapi


app = FastAPI(
    title="Shadow API Engine",
    description="Automated Shadow API discovery and detection engine",
    version="1.0.0",
)


BASE_DIR = Path(__file__).resolve().parent.parent
OPENAPI_FILE = BASE_DIR / "data" / "openapi.yaml"
TRAFFIC_FILE = BASE_DIR / "data" / "observed_traffic.json"


@app.get("/")
def root():
    return {
        "message": "Shadow API Engine is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/discover", response_model=DiscoveryResult)
def discover_shadow_apis():

    # Read documented APIs
    documented = parse_openapi(str(OPENAPI_FILE))

    # Read observed traffic
    with TRAFFIC_FILE.open("r", encoding="utf-8") as file:
        observed_data = json.load(file)

    # Convert traffic data into APIEndpoint objects
    observed = [
        APIEndpoint(
            path=item["path"],
            method=item["method"].upper(),
            source="traffic",
        )
        for item in observed_data
    ]

    # Find undocumented Shadow APIs
    shadow = find_shadow_apis(
        documented,
        observed,
    )

    # Find deprecated APIs still being used
    zombie = find_zombie_apis(
        documented,
        observed,
    )

    # Build complete API inventory
    inventory = build_inventory(
        documented,
        observed,
        shadow,
        zombie,
    )

    return DiscoveryResult(
        documented=documented,
        observed=observed,
        shadow=shadow,
        zombie=zombie,
        inventory=inventory,
    )