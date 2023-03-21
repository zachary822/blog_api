from fastapi import APIRouter, Depends

from api.dependencies import CacheControl, Client
from api.health.schemas import Health, Status

router = APIRouter(tags=["health"])

no_store = CacheControl("must-revalidate, no-store")


@router.get("/", response_model=Health, dependencies=[Depends(no_store)])
async def health(client: Client):
    server_info = await client.server_info()
    return Health(status=Status.ok, mongo_version=server_info["version"])
