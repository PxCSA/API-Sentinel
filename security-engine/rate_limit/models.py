from dataclasses import dataclass


@dataclass
class RateLimitResult:
    allowed: bool
    remaining: int
    limit: int
    reason: str