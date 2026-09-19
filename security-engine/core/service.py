from dataclasses import asdict

from core.engine import SecurityEngine
from core.event_store import SecurityEventStore
from core.events import SecurityEvent


class SecurityEngineService:
    """Public service interface for evaluating API requests."""

    def __init__(self):
        self.engine = SecurityEngine(
            user_objects={
                "user-1": {"obj-1", "obj-2"},
                "user-2": {"obj-3"},
            },
            role_permissions={
                "user": {"/api/profile", "/api/orders"},
                "admin": {"/api/profile", "/api/orders", "/api/admin"},
            },
        )

        self.event_store = SecurityEventStore()

    def evaluate(
        self,
        user_id: str,
        role: str,
        method: str,
        path: str,
        object_id: str | None = None,
    ) -> dict:
        decision = self.engine.evaluate(
            user_id=user_id,
            role=role,
            method=method,
            path=path,
            object_id=object_id,
        )

        decision_dict = asdict(decision)

        event = SecurityEvent.from_decision(
            user_id=user_id,
            role=role,
            method=method,
            path=path,
            object_id=object_id,
            decision=decision_dict,
        )

        self.event_store.add(event)

        return decision_dict

    def get_events(self) -> list[dict]:
        return [asdict(event) for event in self.event_store.get_all()]

    def clear_events(self) -> None:
        self.event_store.clear()