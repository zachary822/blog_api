from typing import Any, Callable, Iterator, Union

import bson
from pydantic import AnyUrl


class MongoDsn(AnyUrl):
    allowed_schemes = {"mongodb", "mongodb+srv"}


class ObjectId(bson.ObjectId):  # type: ignore[misc,name-defined]
    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any], Any]]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[str, "ObjectId", bytes]) -> "ObjectId":
        return cls(v)

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(
            title="_id",
            type="string",
            format="ObjectId",
            example="626b65bb8e5b53965f7c8ae6",
        )
