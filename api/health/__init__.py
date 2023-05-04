from fastapi import APIRouter, Depends

from api.dependencies import CacheControl, Client
from api.health.schemas import Health, Status

no_store = CacheControl("must-revalidate, no-store")

router = APIRouter(tags=["health"], dependencies=[Depends(no_store)])


@router.get("/")
async def health(client: Client) -> Health:
    server_info = await client.server_info()
    return Health(status=Status.ok, mongo_version=server_info["version"])
