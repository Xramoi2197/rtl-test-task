from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    MONGO_USER: str
    MONGO_PASSWORD: SecretStr
    MONGO_HOST: str
    DB_NAME: str
    COLLECTION_NAME: str


config: Settings = Settings()
