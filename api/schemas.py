from datetime import datetime

from pydantic import BaseModel, Field, root_validator

from api.types import ObjectId


class Document(BaseModel):
    id: ObjectId = Field(..., alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class Post(Document):
    title: str
    created: datetime
    body: str


class MonthSummary(BaseModel):
    year: int
    month: int
    count: int

    @root_validator(pre=True)
    def reformat_values(cls, values):
        if "_id" in values:
            return {**values["_id"], **values}
        return values
