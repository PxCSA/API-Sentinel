from .classifier import ThreatClassifier
from .threat import ThreatEvent


def test_classify_bola():
    classifier = ThreatClassifier()

    event = classifier.classify(
        threat_type="BOLA",
        severity="HIGH",
        user_id="user_101",
        path="/api/orders/object_202",
        object_id="object_202",
        reason="User attempted to access an unauthorized object",
    )

    assert event.threat_type == "BOLA"
    assert event.severity == "HIGH"
    assert event.user_id == "user_101"
    assert event.object_id == "object_202"
    assert event.action == "DETECTED"


def test_classify_bfla():
    classifier = ThreatClassifier()

    event = classifier.classify(
        threat_type="BFLA",
        severity="HIGH",
        user_id="user_101",
        path="/api/admin/users",
        object_id=None,
        reason="User role is not authorized to access this function",
    )

    assert event.threat_type == "BFLA"
    assert event.severity == "HIGH"
    assert event.user_id == "user_101"
    assert event.object_id is None
    assert event.action == "DETECTED"