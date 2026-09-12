from dataclasses import asdict

from core.engine import SecurityEngine


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

        return asdict(decision)