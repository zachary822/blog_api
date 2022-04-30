from datetime import datetime

from bson.objectid import ObjectId as _ObjectId
from pydantic import AnyUrl, BaseModel, Field, root_validator


class MongoDsn(AnyUrl):
    allowed_schemes = {"mongodb", "mongodb+srv"}


class ObjectId(_ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return cls(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            title="_id",
            type="string",
            format="ObjectId",
            example="626b65bb8e5b53965f7c8ae6",
        )


class Document(BaseModel):
    id: ObjectId = Field(..., alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class Post(Document):
    title: str
    created: datetime
    body: str


class Month(BaseModel):
    year: int
    month: int
    count: int

    @root_validator(pre=True)
    def reformat_values(cls, values):
        if "_id" in values:
            return {**values["_id"], **values}
        return values
