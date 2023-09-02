from pydantic_settings import BaseSettings, SettingsConfigDict

from api.types import MongoDsn


class Settings(BaseSettings):
    DEBUG: bool = False
    MONGODB_URI: MongoDsn
    ALLOW_ORIGINS: tuple[str] = ("*",)
    ALLOW_METHODS: tuple[str] = ("*",)
    model_config = SettingsConfigDict(env_file=".env", frozen=True)
