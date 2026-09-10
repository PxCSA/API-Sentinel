from typing import Dict, Set

from .models import BFLARequest, BFLAResult


class BFLADetector:
    """Detects function-level authorization violations."""

    def __init__(self, role_permissions: Dict[str, Set[str]]):
        self.role_permissions = role_permissions

    def check(self, request: BFLARequest) -> BFLAResult:
        allowed_paths = self.role_permissions.get(request.role, set())

        if request.path not in allowed_paths:
            return BFLAResult(
                detected=True,
                severity="HIGH",
                reason="User role is not authorized to access this function",
                user_id=request.user_id,
                role=request.role,
                path=request.path,
            )

        return BFLAResult(
            detected=False,
            severity="NONE",
            reason="Function access is authorized",
            user_id=request.user_id,
            role=request.role,
            path=request.path,
        )