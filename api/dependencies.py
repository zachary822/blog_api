from functools import cache
from typing import AsyncIterator, Optional

from fastapi import Depends, Response
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from pydantic import BaseModel, conint

from api.settings import Settings


@cache
def get_settings() -> Settings:
    return Settings()


async def get_client(
    settings: Settings = Depends(get_settings),
) -> AsyncIterator[AsyncIOMotorClient]:
    yield AsyncIOMotorClient(settings.MONGODB_URI)


async def get_fs(client: AsyncIOMotorClient = Depends(get_client)):
    yield AsyncIOMotorGridFSBucket(client.blog)


class CommonQueryParams(BaseModel):
    limit: Optional[conint(le=100, ge=0)] = 10  # type: ignore[valid-type]
    offset: Optional[conint(ge=0)] = 0  # type: ignore[valid-type]


class CacheControl:
    def __init__(self, directives: str):
        self.directives = directives

    async def __call__(self, response: Response) -> None:
        response.headers["Cache-Control"] = self.directives
