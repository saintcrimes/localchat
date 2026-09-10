from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

OS_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):

    database: str
    JWT_SECRET_KEY: str
    JWT_SECRET_REFRESH_KEY: str
    JWT_ALGORITHMS: str
    DB_SCHEMA: str 
    ACCESS_TOKEN_EXPIRE_MINUTE: int


    model_config = SettingsConfigDict(env_file=OS_DIR / ".env", extra="ignore")

settings = Settings()
