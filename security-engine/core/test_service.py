from .service import SecurityEngineService


def test_service_allows_authorized_request():
    service = SecurityEngineService()

    result = service.evaluate(
        user_id="user-1",
        role="user",
        method="GET",
        path="/api/profile",
        object_id="obj-1",
    )

    assert result["allowed"] is True
    assert result["action"] == "ALLOWED"


def test_service_blocks_bola():
    service = SecurityEngineService()

    result = service.evaluate(
        user_id="user-1",
        role="user",
        method="GET",
        path="/api/orders",
        object_id="obj-999",
    )

    assert result["allowed"] is False
    assert result["action"] == "BLOCKED"
    assert result["threat_type"] == "BOLA"


def test_service_blocks_bfla():
    service = SecurityEngineService()

    result = service.evaluate(
        user_id="user-1",
        role="user",
        method="GET",
        path="/api/admin",
    )

    assert result["allowed"] is False
    assert result["action"] == "BLOCKED"
    assert result["threat_type"] == "BFLA"