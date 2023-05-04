from dataclasses import dataclass
from datetime import datetime
from functools import cache
from typing import Annotated, Any, AsyncIterator, Optional

import pendulum
from bson.codec_options import TypeDecoder, TypeRegistry
from fastapi import Depends, Header, Query, Response
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


@cache
def get_client(
    settings: Settings = Depends(get_settings),
) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(
        settings.MONGODB_URI,
        tz_aware=True,
        type_registry=TypeRegistry(type_codecs=[DatetimeDecoder()]),
    )


Client = Annotated[AsyncIOMotorClient, Depends(get_client)]


async def get_db(client: Client) -> AsyncIterator[AsyncIOMotorDatabase]:
    yield client.get_default_database()


Db = Annotated[AsyncIOMotorDatabase, Depends(get_db)]


async def get_session(
    client: Client,
) -> AsyncIterator[AsyncIOMotorClientSession]:
    async with await client.start_session() as s:
        yield s


Session = Annotated[AsyncIOMotorClientSession, Depends(get_session)]


async def get_fs(db: Db):
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


def get_if_none_match(if_none_match: Annotated[str | None, Header()] = None) -> str | None:
    if if_none_match is not None:
        return if_none_match.strip('"')

    return if_none_match


def get_modified_since(if_modified_since: Annotated[str | None, Header()] = None) -> pendulum.DateTime | None:
    if if_modified_since is not None:
        return pendulum.from_format(if_modified_since, "ddd, DD MMM YYYY HH:mm:ss z")

    return if_modified_since
