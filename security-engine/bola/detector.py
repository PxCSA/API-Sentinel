from typing import Dict, Set

from .models import APIRequest, BOLAResult


class BOLADetector:
    """Detects object-level authorization violations."""

    def __init__(self, user_objects: Dict[str, Set[str]]):
        self.user_objects = user_objects

    def check(self, request: APIRequest) -> BOLAResult:
        if request.object_id is None:
            return BOLAResult(
                detected=False,
                severity="NONE",
                reason="No object identifier found in request",
                user_id=request.user_id,
                object_id=None,
            )

        allowed_objects = self.user_objects.get(request.user_id, set())

        if request.object_id not in allowed_objects:
            return BOLAResult(
                detected=True,
                severity="HIGH",
                reason="User attempted to access an unauthorized object",
                user_id=request.user_id,
                object_id=request.object_id,
            )

        return BOLAResult(
            detected=False,
            severity="NONE",
            reason="Object access is authorized",
            user_id=request.user_id,
            object_id=request.object_id,
        )