from .enforcer import Enforcer
from .policy import EnforcementPolicy


def test_high_severity_is_blocked():
    enforcer = Enforcer()

    result = enforcer.enforce("HIGH")

    assert result == "BLOCKED"


def test_medium_severity_is_allowed():
    enforcer = Enforcer()

    result = enforcer.enforce("MEDIUM")

    assert result == "ALLOWED"


def test_low_severity_is_allowed():
    enforcer = Enforcer()

    result = enforcer.enforce("LOW")

    assert result == "ALLOWED"


def test_custom_policy_blocks_medium():
    policy = EnforcementPolicy(block_medium=True)
    enforcer = Enforcer(policy)

    result = enforcer.enforce("MEDIUM")

    assert result == "BLOCKED"