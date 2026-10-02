class EnforcementEngine:

    def enforce(self, security_result: dict):
        if security_result.get("attack") is True:
            return {
                "decision": "BLOCK",
                "allowed": False,
                "attack": True,
                "type": security_result.get("type"),
                "risk": security_result.get("risk"),
                "reason": security_result.get("reason"),
                "owasp_category": security_result.get("owasp_category"),
            }

        return {
            "decision": "ALLOW",
            "allowed": True,
            "attack": False,
            "type": None,
            "risk": None,
            "reason": None,
            "owasp_category": None,
        }
