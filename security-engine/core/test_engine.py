from .engine import SecurityEngine


def test_allowed_request():
    engine = SecurityEngine(
        user_objects={"user-1": {"obj-1"}},
        role_permissions={"user": {"/api/profile"}},
    )

    result = engine.evaluate(
        user_id="user-1",
        role="user",
        method="GET",
        path="/api/profile",
        object_id="obj-1",
    )

    assert result.allowed is True
    assert result.action == "ALLOWED"
    assert result.threat_type is None


def test_bola_request_is_blocked():
    engine = SecurityEngine(
        user_objects={"user-1": {"obj-1"}},
        role_permissions={"user": {"/api/orders"}},
    )

    result = engine.evaluate(
        user_id="user-1",
        role="user",
        method="GET",
        path="/api/orders",
        object_id="obj-999",
    )

    assert result.allowed is False
    assert result.action == "BLOCKED"
    assert result.threat_type == "BOLA"


def test_bfla_request_is_blocked():
    engine = SecurityEngine(
        user_objects={"user-1": {"obj-1"}},
        role_permissions={"user": {"/api/profile"}},
    )

    result = engine.evaluate(
        user_id="user-1",
        role="user",
        method="GET",
        path="/api/admin",
    )

    assert result.allowed is False
    assert result.action == "BLOCKED"
    assert result.threat_type == "BFLA"