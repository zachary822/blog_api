from bson import ObjectId
from starlette.convertors import Convertor, register_url_convertor


class ObjectIdConverter(Convertor):
    regex = r"[0-9a-fA-F]{24}"

    def convert(self, value: str) -> ObjectId:
        return ObjectId(value)

    def to_string(self, value) -> str:
        return str(value)


register_url_convertor("oid", ObjectIdConverter())
