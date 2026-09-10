
from dataclasses import dataclass


@dataclass
class BFLARequest:
    user_id: str
    role: str
    method: str
    path: str


@dataclass
class BFLAResult:
    detected: bool
    severity: str
    reason: str
    user_id: str
    role: str
    path: str
