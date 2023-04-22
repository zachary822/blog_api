from enum import Enum

import strawberry

from api.schemas import CustomBaseModel


@strawberry.enum
class Status(str, Enum):
    ok = "ok"
    bad = "bad"


class Health(CustomBaseModel):
    status: Status
    mongo_version: str
