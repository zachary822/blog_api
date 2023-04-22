from typing import Optional

import orjson
from pendulum import DateTime
from pydantic import AnyHttpUrl, BaseModel, Field

from api.types import ObjectId


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class CustomBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Document(CustomBaseModel):
    id: ObjectId = Field(..., alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class Post(Document):
    title: str
    created: DateTime
    updated: DateTime
    image: Optional[AnyHttpUrl]
    summary: Optional[str]
    body: str
    tags: list[str] = Field(default_factory=list)


class MonthSummary(CustomBaseModel):
    year: int
    month: int
    count: int


class TagSummary(CustomBaseModel):
    name: str
    count: int


class Summary(CustomBaseModel):
    monthly: list[MonthSummary]
    tags: list[TagSummary]
