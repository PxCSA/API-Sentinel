import time
from typing import Dict

from .models import RateLimitResult


class RateLimiter:
    """Simple in-memory per-client rate limiter."""

    def __init__(self, limit: int = 10, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests: Dict[str, list[float]] = {}

    def check(self, client_id: str) -> RateLimitResult:
        now = time.time()
        timestamps = self.requests.get(client_id, [])

        timestamps = [
            timestamp
            for timestamp in timestamps
            if now - timestamp < self.window_seconds
        ]

        if len(timestamps) >= self.limit:
            self.requests[client_id] = timestamps
            return RateLimitResult(
                allowed=False,
                remaining=0,
                limit=self.limit,
                reason="Rate limit exceeded",
            )

        timestamps.append(now)
        self.requests[client_id] = timestamps

        return RateLimitResult(
            allowed=True,
            remaining=self.limit - len(timestamps),
            limit=self.limit,
            reason="Request allowed",
        )