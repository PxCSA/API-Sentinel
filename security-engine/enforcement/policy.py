from dataclasses import dataclass


@dataclass
class EnforcementPolicy:
    block_high: bool = True
    block_medium: bool = False
    block_low: bool = False

    def should_block(self, severity: str) -> bool:
        severity = severity.upper()

        if severity == "HIGH":
            return self.block_high

        if severity == "MEDIUM":
            return self.block_medium

        if severity == "LOW":
            return self.block_low

        return False