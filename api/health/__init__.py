from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from api.dependencies import get_client
from api.health.schemas import Health, Status

router = APIRouter(tags=["health"])


@router.get("/", response_model=Health)
async def health(client: AsyncIOMotorClient = Depends(get_client)):
    server_info = await client.server_info()
    return Health(status=Status.ok, mongo_version=server_info["version"])
