from typing import Annotated, Any, Callable

import pendulum
from bson import ObjectId
from pydantic import AnyUrl, GetJsonSchemaHandler, UrlConstraints
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

MongoDsn = Annotated[AnyUrl, UrlConstraints(host_required=True, allowed_schemes=["mongodb", "mongodb+srv"])]


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Callable[[Any], core_schema.CoreSchema]
    ) -> core_schema.CoreSchema:
        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(pattern=r"[0-9a-fA-F]{24}"),
                core_schema.no_info_plain_validator_function(ObjectId),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_str_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema(pattern=r"[0-9a-fA-F]{24}"))


class _DateTimePydanticAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Callable[[Any], core_schema.CoreSchema]
    ) -> core_schema.CoreSchema:
        from_datetime_schema = core_schema.chain_schema(
            [
                core_schema.datetime_schema(),
                core_schema.no_info_plain_validator_function(pendulum.instance),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_datetime_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(pendulum.DateTime),
                    from_datetime_schema,
                ]
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.datetime_schema())


PydanticDateTime = Annotated[pendulum.DateTime, _DateTimePydanticAnnotation]
