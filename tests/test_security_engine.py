from pathlib import Path
from fastapi.testclient import TestClient
from importlib.machinery import SourceFileLoader

from app.main import app


SecurityEngine = SourceFileLoader(
    "security_engine_test",
    "security-engine/security_engine.py"
).load_module().SecurityEngine


def test_allowed_request():
    engine = SecurityEngine()

    engine.bola.register_object("user1", "101")
    engine.bfla.register_permission("user", "GET", "/users")

    result = engine.check_request(
        user_id="user1",
        role="user",
        method="GET",
        path="/users",
        object_id="101",
    )

    assert result["decision"] == "ALLOW"
    assert result["allowed"] is True
    assert result["attack"] is False


def test_bola_attack():
    engine = SecurityEngine()

    engine.bola.register_object("user1", "101")
    engine.bfla.register_permission("user", "GET", "/users")

    result = engine.check_request(
        user_id="user1",
        role="user",
        method="GET",
        path="/users",
        object_id="999",
    )

    assert result["decision"] == "BLOCK"
    assert result["type"] == "BOLA"
    assert result["risk"] == "HIGH"
    assert result["owasp_category"] == (
        "API1:2023 - Broken Object Level Authorization"
    )


def test_bfla_attack():
    engine = SecurityEngine()

    engine.bola.register_object("user1", "101")
    engine.bfla.register_permission("user", "GET", "/users")

    result = engine.check_request(
        user_id="user1",
        role="user",
        method="DELETE",
        path="/users/{id}",
        object_id="101",
    )

    assert result["decision"] == "BLOCK"
    assert result["type"] == "BFLA"
    assert result["risk"] == "HIGH"
    assert result["owasp_category"] == (
        "API5:2023 - Broken Function Level Authorization"
    )


def test_rate_limit():
    engine = SecurityEngine()

    engine.bfla.register_permission("user", "GET", "/users")

    for _ in range(3):
        result = engine.check_request(
            user_id="rateuser",
            role="user",
            method="GET",
            path="/users",
        )
        assert result["decision"] == "ALLOW"

    result = engine.check_request(
        user_id="rateuser",
        role="user",
        method="GET",
        path="/users",
    )

    assert result["decision"] == "BLOCK"
    assert result["type"] == "RATE_LIMIT"
    assert result["risk"] == "MEDIUM"
    assert result["owasp_category"] == (
        "API4:2023 - Unrestricted Resource Consumption"
    )


def test_fastapi_security_check():
    client = TestClient(app)

    response = client.post(
        "/api/security-check"
        "?user_id=apiuser"
        "&role=unknown"
        "&method=GET"
        "&path=/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["decision"] == "BLOCK"
    assert data["allowed"] is False
    assert data["attack"] is True
    assert data["type"] == "BFLA"
    assert data["risk"] == "HIGH"
