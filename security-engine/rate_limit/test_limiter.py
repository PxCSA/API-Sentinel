from .limiter import RateLimiter


def test_requests_allowed_within_limit():
    limiter = RateLimiter(limit=3, window_seconds=60)

    result = limiter.check("client-1")
    assert result.allowed is True
    assert result.remaining == 2

    result = limiter.check("client-1")
    assert result.allowed is True
    assert result.remaining == 1


def test_request_blocked_after_limit():
    limiter = RateLimiter(limit=2, window_seconds=60)

    limiter.check("client-1")
    limiter.check("client-1")

    result = limiter.check("client-1")

    assert result.allowed is False
    assert result.remaining == 0
    assert result.reason == "Rate limit exceeded"


def test_clients_are_tracked_separately():
    limiter = RateLimiter(limit=1, window_seconds=60)

    first = limiter.check("client-1")
    second = limiter.check("client-2")

    assert first.allowed is True
    assert second.allowed is True