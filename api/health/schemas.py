from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    ok = "ok"
    bad = "bad"


class Health(BaseModel):
    status: Status
    mongo_version: str
