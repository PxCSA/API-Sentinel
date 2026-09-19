from dataclasses import dataclass
from datetime import datetime


@dataclass
class SecurityEvent:
    timestamp: str
    user_id: str
    role: str
    method: str
    path: str
    object_id: str | None
    allowed: bool
    action: str
    threat_type: str | None
    severity: str
    reason: str

    @classmethod
    def from_decision(
        cls,
        user_id: str,
        role: str,
        method: str,
        path: str,
        object_id: str | None,
        decision: dict,
    ) -> "SecurityEvent":
        return cls(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            user_id=user_id,
            role=role,
            method=method,
            path=path,
            object_id=object_id,
            allowed=decision["allowed"],
            action=decision["action"],
            threat_type=decision["threat_type"],
            severity=decision["severity"],
            reason=decision["reason"],
        )