from datetime import datetime
from typing import Optional

import strawberry

from api.health import Status


@strawberry.type
class Post:
    id: str
    title: str
    created: datetime
    updated: datetime
    image: Optional[str] = None
    body: str
    tags: list[str]
    summary: Optional[str] = None

    @classmethod
    def from_db_model(cls, post: dict):
        match post:
            case {"_id": _id, **rest}:
                return cls(id=_id, **rest)  # type: ignore[call-arg]
            case _:
                raise ValueError("malformed post")


@strawberry.type
class Health:
    status: Status
    mongo_version: str
