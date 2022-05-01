from functools import cache
from typing import AsyncIterator, Optional

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, conint

from api.settings import Settings


@cache
def get_settings() -> Settings:
    return Settings()


async def get_client(
    settings: Settings = Depends(get_settings),
) -> AsyncIterator[AsyncIOMotorClient]:
    yield AsyncIOMotorClient(settings.MONGODB_URI)


class CommonQueryParams(BaseModel):
    limit: Optional[conint(le=100, ge=0)] = 10  # type: ignore[valid-type]
    offset: Optional[conint(ge=0)] = 0  # type: ignore[valid-type]
