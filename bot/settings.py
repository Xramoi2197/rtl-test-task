from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr


config: Settings = Settings()
