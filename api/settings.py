from typing import Optional

from pydantic import BaseSettings

from api.types import MongoDsn


class Settings(BaseSettings):
    MONGODB_URI: Optional[MongoDsn]
    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_METHODS: list[str] = ["*"]

    class Config:
        env_file = ".env"
