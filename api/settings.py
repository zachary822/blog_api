from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, FilePath

from api.types import MongoDsn


class Settings(BaseSettings):
    MONGODB_URI: Optional[MongoDsn]
    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_METHODS: list[str] = ["*"]
    LOGGING_CONFIG: FilePath = Path(__file__).resolve().parents[1] / "logging.conf"

    class Config:
        env_file = ".env"
