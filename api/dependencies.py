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
from api.utils import DirectiveMap


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


def get_if_none_match(if_none_match: Annotated[str | None, Header()] = None) -> str | None:
    if if_none_match is not None:
        return if_none_match.strip('"')

    return if_none_match


def get_if_modified_since(if_modified_since: Annotated[str | None, Header()] = None) -> pendulum.DateTime | None:
    if if_modified_since is not None:
        return pendulum.from_format(if_modified_since, "ddd, DD MMM YYYY HH:mm:ss z")

    return if_modified_since


class CacheControl:
    def __init__(self, directives: str | None = None):
        self.directives = directives

    async def __call__(
        self,
        response: Response,
        cache_control: Annotated[str | None, Header()] = None,
        if_none_match: None | str = Depends(get_if_none_match),
        if_modified_since: datetime | None = Depends(get_if_modified_since),
    ):
        if self.directives is not None:
            # Does not work if returning custom responses
            response.headers["Cache-Control"] = self.directives

        def _is_not_modified(etag: str | None = None, modified_since: datetime | None = None) -> bool:
            request_directives = DirectiveMap(cache_control)

            if request_directives["no-cache"]:
                return False

            return (not (if_none_match is None or etag is None) and if_none_match == etag) or (
                not (if_modified_since is None or modified_since is None) and modified_since > if_modified_since
            )

        yield _is_not_modified
