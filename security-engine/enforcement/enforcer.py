from typing import Optional

from .policy import EnforcementPolicy


class Enforcer:
    """Applies enforcement decisions to detected threats."""

    def __init__(self, policy: Optional[EnforcementPolicy] = None):
        self.policy = policy or EnforcementPolicy()

    def enforce(self, severity: str) -> str:
        if self.policy.should_block(severity):
            return "BLOCKED"

        return "ALLOWED"