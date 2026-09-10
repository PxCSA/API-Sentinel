from .detector import BOLADetector
from .models import APIRequest


def test_allowed_object():
    user_objects = {
        "user_101": {"object_101", "object_102"},
        "user_202": {"object_201", "object_202"},
    }

    detector = BOLADetector(user_objects)

    request = APIRequest(
        user_id="user_101",
        object_id="object_101",
        method="GET",
        path="/api/orders/object_101",
    )

    result = detector.check(request)

    assert result.detected is False
    assert result.severity == "NONE"


def test_unauthorized_object():
    user_objects = {
        "user_101": {"object_101", "object_102"},
        "user_202": {"object_201", "object_202"},
    }

    detector = BOLADetector(user_objects)

    request = APIRequest(
        user_id="user_101",
        object_id="object_202",
        method="GET",
        path="/api/orders/object_202",
    )

    result = detector.check(request)

    assert result.detected is True
    assert result.severity == "HIGH"