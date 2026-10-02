class BFLAEngine:
    def __init__(self):
        self.role_permissions = {}

    def register_permission(self, role: str, method: str, path: str):
        if role not in self.role_permissions:
            self.role_permissions[role] = set()

        self.role_permissions[role].add(
            (method.upper(), path)
        )

    def check_access(self, role: str, method: str, path: str):
        key = (method.upper(), path)

        allowed_functions = self.role_permissions.get(role, set())

        if key in allowed_functions:
            return {
                "allowed": True,
                "attack": False,
                "type": None,
                "role": role,
                "method": method.upper(),
                "path": path,
            }

        return {
            "allowed": False,
            "attack": True,
            "type": "BFLA",
            "role": role,
            "method": method.upper(),
            "path": path,
            "risk": "HIGH",
            "reason": "Role attempted to access a function that is not permitted.",
            "owasp_category": "API5:2023 - Broken Function Level Authorization",
        }
