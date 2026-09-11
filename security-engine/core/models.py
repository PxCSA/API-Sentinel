from dataclasses import dataclass
from typing import Optional


@dataclass
class SecurityDecision:
    allowed: bool
    action: str
    threat_type: Optional[str]
    severity: str
    reason: str