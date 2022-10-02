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
    image: Optional[AnyHttpUrl]
    body: str


class MonthSummary(BaseModel):
    year: int
    month: int
    count: int
