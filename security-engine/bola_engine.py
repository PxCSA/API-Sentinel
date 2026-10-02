from collections import defaultdict


class BOLAEngine:
    def __init__(self):
        self.user_objects = defaultdict(set)

    def register_object(self, user_id: str, object_id: str):
        self.user_objects[user_id].add(object_id)

    def check_access(self, user_id: str, object_id: str):
        allowed_objects = self.user_objects.get(user_id, set())

        if object_id in allowed_objects:
            return {
                "allowed": True,
                "attack": False,
                "type": None,
                "user_id": user_id,
                "object_id": object_id,
            }

        return {
            "allowed": False,
            "attack": True,
            "type": "BOLA",
            "user_id": user_id,
            "object_id": object_id,
            "risk": "HIGH",
            "reason": "User attempted to access an object that is not assigned to them.",
            "owasp_category": "API1:2023 - Broken Object Level Authorization",
        }
