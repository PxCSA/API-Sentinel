from threading import Lock

from core.events import SecurityEvent


class SecurityEventStore:
    """In-memory storage for security events."""

    def __init__(self, max_events: int = 1000):
        self.max_events = max_events
        self._events: list[SecurityEvent] = []
        self._lock = Lock()

    def add(self, event: SecurityEvent) -> None:
        with self._lock:
            self._events.append(event)

            if len(self._events) > self.max_events:
                self._events = self._events[-self.max_events:]

    def get_all(self) -> list[SecurityEvent]:
        with self._lock:
            return list(self._events)

    def get_stats(self) -> dict:
        with self._lock:
            total_requests = len(self._events)

            allowed_requests = sum(
                1 for event in self._events
                if event.allowed
            )

            blocked_requests = sum(
                1 for event in self._events
                if not event.allowed
            )

            bola_attacks = sum(
                1 for event in self._events
                if event.threat_type == "BOLA"
            )

            bfla_attacks = sum(
                1 for event in self._events
                if event.threat_type == "BFLA"
            )

            rate_limit_violations = sum(
                1 for event in self._events
                if event.threat_type == "RATE_LIMIT"
            )

            return {
                "total_requests": total_requests,
                "allowed_requests": allowed_requests,
                "blocked_requests": blocked_requests,
                "bola_attacks": bola_attacks,
                "bfla_attacks": bfla_attacks,
                "rate_limit_violations": rate_limit_violations,
            }

    def clear(self) -> None:
        with self._lock:
            self._events.clear()