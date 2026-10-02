import time


class RateLimiter:
    def __init__(self, max_requests: int = 3, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    def check_request(self, user_id: str):
        current_time = time.time()

        request_times = self.requests.get(user_id, [])

        request_times = [
            timestamp
            for timestamp in request_times
            if current_time - timestamp < self.window_seconds
        ]

        if len(request_times) >= self.max_requests:
            self.requests[user_id] = request_times

            return {
                "allowed": False,
                "blocked": True,
                "user_id": user_id,
                "reason": "Rate limit exceeded.",
                "risk": "MEDIUM",
            }

        request_times.append(current_time)
        self.requests[user_id] = request_times

        return {
            "allowed": True,
            "blocked": False,
            "user_id": user_id,
            "remaining": self.max_requests - len(request_times),
        }
