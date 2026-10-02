from importlib.machinery import SourceFileLoader

BOLAEngine = SourceFileLoader(
    "bola_engine",
    "security-engine/bola_engine.py"
).load_module().BOLAEngine

BFLAEngine = SourceFileLoader(
    "bfla_engine",
    "security-engine/bfla_engine.py"
).load_module().BFLAEngine

EnforcementEngine = SourceFileLoader(
    "enforcement",
    "security-engine/enforcement.py"
).load_module().EnforcementEngine

RateLimiter = SourceFileLoader(
    "rate_limiter",
    "security-engine/rate_limiter.py"
).load_module().RateLimiter


class SecurityEngine:

    def __init__(self):
        self.bola = BOLAEngine()
        self.bfla = BFLAEngine()
        self.rate_limiter = RateLimiter()
        self.enforcement = EnforcementEngine()

    def check_request(
        self,
        user_id: str,
        role: str,
        method: str,
        path: str,
        object_id: str = None,
    ):
        rate_result = self.rate_limiter.check_request(user_id)

        if rate_result["blocked"]:
            return self.enforcement.enforce({
                "attack": True,
                "type": "RATE_LIMIT",
                "risk": rate_result["risk"],
                "reason": rate_result["reason"],
                "owasp_category": "API4:2023 - Unrestricted Resource Consumption",
            })

        if object_id is not None:
            bola_result = self.bola.check_access(
                user_id,
                object_id,
            )

            if bola_result["attack"]:
                return self.enforcement.enforce(bola_result)

        bfla_result = self.bfla.check_access(
            role,
            method,
            path,
        )

        if bfla_result["attack"]:
            return self.enforcement.enforce(bfla_result)

        return self.enforcement.enforce({
            "attack": False
        })
