from typing import Dict, Set

from bola.detector import BOLADetector
from bola.models import APIRequest
from bfla.detector import BFLADetector
from bfla.models import BFLARequest
from detection.classifier import ThreatClassifier
from enforcement.enforcer import Enforcer
from rate_limit.limiter import RateLimiter
from .models import SecurityDecision


class SecurityEngine:
    """Coordinates rate limiting, BOLA, BFLA, classification, and enforcement."""

    def __init__(
        self,
        user_objects: Dict[str, Set[str]],
        role_permissions: Dict[str, Set[str]],
    ):
        self.bola = BOLADetector(user_objects)
        self.bfla = BFLADetector(role_permissions)
        self.classifier = ThreatClassifier()
        self.enforcer = Enforcer()
        self.rate_limiter = RateLimiter()

    def evaluate(
        self,
        user_id: str,
        role: str,
        method: str,
        path: str,
        object_id: str | None = None,
    ) -> SecurityDecision:

        rate_result = self.rate_limiter.check(user_id)

        if not rate_result.allowed:
            return SecurityDecision(
                allowed=False,
                action="BLOCKED",
                threat_type="RATE_LIMIT",
                severity="HIGH",
                reason=rate_result.reason,
            )

        bola_result = self.bola.check(
            APIRequest(
                user_id=user_id,
                object_id=object_id,
                method=method,
                path=path,
                role=role,
            )
        )

        if bola_result.detected:
            event = self.classifier.classify(
                threat_type="BOLA",
                severity=bola_result.severity,
                user_id=bola_result.user_id,
                path=path,
                object_id=bola_result.object_id,
                reason=bola_result.reason,
            )

            action = self.enforcer.enforce(event.severity)

            return SecurityDecision(
                allowed=action != "BLOCKED",
                action=action,
                threat_type=event.threat_type,
                severity=event.severity,
                reason=event.reason,
            )

        bfla_result = self.bfla.check(
            BFLARequest(
                user_id=user_id,
                role=role,
                method=method,
                path=path,
            )
        )

        if bfla_result.detected:
            event = self.classifier.classify(
                threat_type="BFLA",
                severity=bfla_result.severity,
                user_id=bfla_result.user_id,
                path=bfla_result.path,
                object_id=None,
                reason=bfla_result.reason,
            )

            action = self.enforcer.enforce(event.severity)

            return SecurityDecision(
                allowed=action != "BLOCKED",
                action=action,
                threat_type=event.threat_type,
                severity=event.severity,
                reason=event.reason,
            )

        return SecurityDecision(
            allowed=True,
            action="ALLOWED",
            threat_type=None,
            severity="NONE",
            reason="Request passed security checks",
        )