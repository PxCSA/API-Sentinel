from dataclasses import dataclass
from typing import Optional


@dataclass
class APIRequest:
    user_id: str
    object_id: Optional[str]
    method: str
    path: str
    role: str = "user"


@dataclass
class BOLAResult:
    detected: bool
    severity: str
    reason: str
    user_id: str
    object_id: Optional[str]
