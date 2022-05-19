from dataclasses import dataclass
from datetime import datetime
from functools import cache
from typing import Any, AsyncIterator, Optional

import pendulum
from async_lru import alru_cache
from bson.codec_options import TypeDecoder, TypeRegistry
from fastapi import Depends, Query, Response
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorDatabase,
    AsyncIOMotorGridFSBucket,
)
from pydantic import conint, constr

from api.settings import Settings


class DatetimeDecoder(TypeDecoder):
    bson_type = datetime

    def transform_bson(self, value: Any) -> Any:
        return pendulum.instance(value)


@cache
def get_settings() -> Settings:
    return Settings()


@alru_cache
async def get_client(
    settings: Settings = Depends(get_settings),
) -> AsyncIterator[AsyncIOMotorClient]:
    return AsyncIOMotorClient(
        settings.MONGODB_URI,
        tz_aware=True,
        type_registry=TypeRegistry(type_codecs=[DatetimeDecoder()]),
    )


async def get_db(client=Depends(get_client)) -> AsyncIterator[AsyncIOMotorDatabase]:
    yield client.get_default_database()


async def get_session(
    client: AsyncIOMotorClient = Depends(get_client),
) -> AsyncIterator[AsyncIOMotorClientSession]:
    async with await client.start_session() as s:
        yield s


async def get_fs(db: AsyncIOMotorDatabase = Depends(get_db)):
    return AsyncIOMotorGridFSBucket(db)


@dataclass
class CommonQueryParams:
    q: Optional[constr(strip_whitespace=True, min_length=1)] = Query(  # type: ignore[valid-type]
        None, description="search post"
    )
    limit: Optional[conint(le=100, ge=1)] = 10  # type: ignore[valid-type]
    offset: Optional[conint(ge=0)] = 0  # type: ignore[valid-type]


class CacheControl:
    def __init__(self, directives: str):
        self.directives = directives

    async def __call__(self, response: Response) -> None:
        response.headers["Cache-Control"] = self.directives
