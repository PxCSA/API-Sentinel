from typing import Optional

from .threat import ThreatEvent


class ThreatClassifier:
    """Converts security detection results into normalized threat events."""

    def classify(
        self,
        threat_type: str,
        severity: str,
        user_id: Optional[str],
        path: str,
        object_id: Optional[str],
        reason: str,
    ) -> ThreatEvent:
        return ThreatEvent(
            threat_type=threat_type,
            severity=severity,
            user_id=user_id,
            path=path,
            object_id=object_id,
            reason=reason,
        )