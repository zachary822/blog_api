from bson import ObjectId as _ObjectId
from pydantic import AnyUrl


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
