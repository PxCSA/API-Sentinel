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

    def clear(self) -> None:
        with self._lock:
            self._events.clear()