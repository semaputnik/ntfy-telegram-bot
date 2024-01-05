from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', extra='ignore')

    token: str = Field(alias="TELEGRAM_BOT_TOKEN")
    host: str = Field(alias="HOST")
    port: str = Field(alias="PORT")
    topics_raw_string: str = Field(alias="TOPICS")
    chat_id: str = Field(alias="CHAT_ID", default="")

    @property
    def base_url(self):
        return f"ws://{self.host}:{self.port}/{{}}/ws"

    @property
    def topics(self) -> list[str]:
        return self.topics_raw_string.split(",")

    BASE_DIR: Path = Path(__file__).resolve().parent
    LOGGING_FILE_PATH: Path = BASE_DIR / "logging.ini"
    ROOT_DIR: Path = BASE_DIR.parent
    LOGS_DIR: Path = ROOT_DIR / "logs"
    TEMPLATES_DIR: Path = BASE_DIR / "."
