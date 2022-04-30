from fastapi import APIRouter

from api.health.schemas import Health, Status

router = APIRouter(tags=["health"])


@router.get("/", response_model=Health)
def health():
    return Health(status=Status.ok)
