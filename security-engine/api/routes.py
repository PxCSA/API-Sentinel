from fastapi import APIRouter

from core.service import SecurityEngineService

router = APIRouter()
security_service = SecurityEngineService()


@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/evaluate")
def evaluate(
    user_id: str,
    role: str,
    method: str,
    path: str,
    object_id: str | None = None,
):
    return security_service.evaluate(
        user_id=user_id,
        role=role,
        method=method,
        path=path,
        object_id=object_id,
    )