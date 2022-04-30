from fastapi import APIRouter
from health.schemas import Health, Status

router = APIRouter(tags=["health"])


@router.get("/health", response_model=Health)
def health():
    return Health(status=Status.ok)
