from pydantic import BaseSettings

from api.types import MongoDsn


class Settings(BaseSettings):
    DEBUG: bool = False
    MONGODB_URI: MongoDsn
    ALLOW_ORIGINS: tuple[str] = ("*",)
    ALLOW_METHODS: tuple[str] = ("*",)

    class Config:
        env_file = ".env"
        frozen = True
