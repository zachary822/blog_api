from typing import Optional

from pendulum import DateTime
from pydantic import AnyHttpUrl, BaseModel, Field

from api.types import ObjectId


class Document(BaseModel):
    id: ObjectId = Field(..., alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class Post(Document):
    title: str
    created: DateTime
    updated: DateTime
    image: Optional[AnyHttpUrl]
    body: str
    tags: list[str] = Field(default_factory=list)


class MonthSummary(BaseModel):
    year: int
    month: int
    count: int


class TagSummary(BaseModel):
    name: str
    count: int


class Summary(BaseModel):
    monthly: list[MonthSummary]
    tags: list[TagSummary]
