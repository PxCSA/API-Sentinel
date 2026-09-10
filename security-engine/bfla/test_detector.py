from .detector import BFLADetector
from .models import BFLARequest


def test_allowed_function():
    role_permissions = {
        "user": {"/api/profile", "/api/orders"},
        "admin": {"/api/profile", "/api/orders", "/api/admin/users"},
    }

    detector = BFLADetector(role_permissions)

    request = BFLARequest(
        user_id="user_101",
        role="user",
        method="GET",
        path="/api/profile",
    )

    result = detector.check(request)

    assert result.detected is False
    assert result.severity == "NONE"


def test_unauthorized_function():
    role_permissions = {
        "user": {"/api/profile", "/api/orders"},
        "admin": {"/api/profile", "/api/orders", "/api/admin/users"},
    }

    detector = BFLADetector(role_permissions)

    request = BFLARequest(
        user_id="user_101",
        role="user",
        method="GET",
        path="/api/admin/users",
    )

    result = detector.check(request)

    assert result.detected is True
    assert result.severity == "HIGH"