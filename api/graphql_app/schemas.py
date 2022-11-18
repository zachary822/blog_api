from datetime import datetime
from typing import Optional

import strawberry


@strawberry.type
class Post:
    id: str
    title: str
    created: datetime
    updated: datetime
    image: Optional[str] = None
    body: str
    tags: list[str]

    @classmethod
    def from_db_model(cls, post: dict):
        match post:
            case {"_id": _id, "published": True, **rest}:
                return cls(id=_id, **rest)  # type: ignore[call-arg]
            case _:
                raise ValueError("malformed post")
