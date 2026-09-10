from dataclasses import dataclass
from typing import Optional


@dataclass
class ThreatEvent:
    threat_type: str
    severity: str
    user_id: Optional[str]
    path: str
    object_id: Optional[str]
    reason: str
    action: str = "DETECTED"