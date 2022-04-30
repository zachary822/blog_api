from typing import Optional

from pydantic import BaseSettings

from api.types import MongoDsn


class Settings(BaseSettings):
    MONGODB_URI: MongoDsn
    ALLOW_ORIGINS: Optional[list[str]] = ["*"]
    ALLOW_METHODS: Optional[list[str]] = ["*"]

    class Config:
        env_file = ".env"
