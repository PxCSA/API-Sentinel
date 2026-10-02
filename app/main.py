from pathlib import Path
from fastapi import FastAPI

from .discovery_engine import (
    find_shadow_apis,
    find_zombie_apis,
    build_inventory,
)
from .models import DiscoveryResult, TrafficRequest
from .openapi_parser import parse_openapi
from .traffic_parser import (
    parse_traffic,
    parse_traffic_records,
    deduplicate_traffic,
)

from importlib.machinery import SourceFileLoader


SecurityEngine = SourceFileLoader(
    "security_engine",
    str(
        Path(__file__).resolve().parent.parent
        / "security-engine"
        / "security_engine.py"
    ),
).load_module().SecurityEngine


app = FastAPI(
    title="Shadow API Engine",
    description="Automated Shadow API discovery and detection engine",
    version="1.0.0",
)

BASE_DIR = Path(__file__).resolve().parent.parent
OPENAPI_FILE = BASE_DIR / "data" / "openapi.yaml"
TRAFFIC_FILE = BASE_DIR / "data" / "observed_traffic.json"

traffic_buffer = []
security_engine = SecurityEngine()


@app.get("/")
def root():
    return {"message": "Shadow API Engine is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/traffic")
def receive_traffic(request: TrafficRequest):
    records = parse_traffic_records([request.model_dump()])
    traffic_buffer.extend(records)

    return {
        "message": "Traffic received successfully",
        "received": len(records),
    }


@app.get("/discover", response_model=DiscoveryResult)
def discover_shadow_apis():
    documented = parse_openapi(str(OPENAPI_FILE))

    observed = parse_traffic(str(TRAFFIC_FILE))
    observed.extend(traffic_buffer)
    observed = deduplicate_traffic(observed)

    shadow = find_shadow_apis(documented, observed)
    zombie = find_zombie_apis(documented, observed)

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


@app.get("/api/traffic")
def get_traffic():
    observed = parse_traffic(str(TRAFFIC_FILE))
    observed.extend(traffic_buffer)
    observed = deduplicate_traffic(observed)

    return {
        "count": len(observed),
        "traffic": observed,
    }


@app.get("/api/inventory")
def get_inventory():
    documented = parse_openapi(str(OPENAPI_FILE))

    observed = parse_traffic(str(TRAFFIC_FILE))
    observed.extend(traffic_buffer)
    observed = deduplicate_traffic(observed)

    shadow = find_shadow_apis(documented, observed)
    zombie = find_zombie_apis(documented, observed)

    inventory = build_inventory(
        documented,
        observed,
        shadow,
        zombie,
    )

    return {
        "count": len(inventory),
        "inventory": inventory,
    }


@app.get("/api/security-alerts")
def get_security_alerts():
    documented = parse_openapi(str(OPENAPI_FILE))

    observed = parse_traffic(str(TRAFFIC_FILE))
    observed.extend(traffic_buffer)
    observed = deduplicate_traffic(observed)

    shadow = find_shadow_apis(documented, observed)
    zombie = find_zombie_apis(documented, observed)

    alerts = []

    for endpoint in shadow:
        alerts.append({
            "type": "SHADOW_API",
            "path": endpoint.path,
            "method": endpoint.method,
            "risk": endpoint.risk,
            "reason": endpoint.reason,
        })

    for endpoint in zombie:
        alerts.append({
            "type": "ZOMBIE_API",
            "path": endpoint.path,
            "method": endpoint.method,
            "risk": endpoint.risk,
            "reason": endpoint.reason,
        })

    return {
        "count": len(alerts),
        "alerts": alerts,
    }


@app.get("/api/statistics")
def get_statistics():
    documented = parse_openapi(str(OPENAPI_FILE))

    observed = parse_traffic(str(TRAFFIC_FILE))
    observed.extend(traffic_buffer)
    observed = deduplicate_traffic(observed)

    shadow = find_shadow_apis(documented, observed)
    zombie = find_zombie_apis(documented, observed)

    active_count = sum(
        1
        for endpoint in documented
        if not endpoint.deprecated
        and any(
            endpoint.method.upper() == observed_endpoint.method.upper()
            and endpoint.path == observed_endpoint.path
            for observed_endpoint in observed
        )
    )

    deprecated_count = sum(
        1 for endpoint in documented if endpoint.deprecated
    )

    high_risk_count = sum(
        1 for endpoint in shadow if endpoint.risk == "HIGH"
    )

    medium_risk_count = sum(
        1
        for endpoint in shadow + zombie
        if endpoint.risk == "MEDIUM"
    )

    return {
        "total_documented": len(documented),
        "total_observed": len(observed),
        "active": active_count,
        "deprecated": deprecated_count,
        "shadow": len(shadow),
        "zombie": len(zombie),
        "high_risk": high_risk_count,
        "medium_risk": medium_risk_count,
    }


@app.post("/api/security-check")
def security_check(
    user_id: str,
    role: str,
    method: str,
    path: str,
    object_id: str = None,
):
    return security_engine.check_request(
        user_id=user_id,
        role=role,
        method=method,
        path=path,
        object_id=object_id,
    )
