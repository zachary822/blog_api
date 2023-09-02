from typing import Optional

from pydantic import AnyHttpUrl, BaseModel, Field

from api.types import PydanticDateTime, PydanticObjectId


class CustomBaseModel(BaseModel):
    ...


class Document(CustomBaseModel):
    id: PydanticObjectId = Field(..., alias="_id")


class Post(Document):
    title: str
    created: PydanticDateTime
    updated: PydanticDateTime
    image: Optional[AnyHttpUrl] = None
    summary: Optional[str] = None
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
