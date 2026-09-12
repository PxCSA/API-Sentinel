from core.service import SecurityEngineService


def test_rate_limit_blocks_excessive_requests():
    service = SecurityEngineService()

    service.engine.rate_limiter = None