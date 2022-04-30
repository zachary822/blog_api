from pydantic import BaseSettings

from schemas import MongoDsn
from typing import Optional


class Settings(BaseSettings):
    MONGODB_URI: MongoDsn
    ALLOW_ORIGINS: Optional[list[str]] = ["*"]
    ALLOW_METHODS: Optional[list[str]] = ["*"]

    class Config:
        env_file = ".env"
