import os
from decimal import ROUND_HALF_UP

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Banking rounding
    ROUNDING: str = ROUND_HALF_UP

    DATE_FORMAT: str
    DB_URL: str
    TEST_DB_URL: str
    DEFAULT_CREDIT_LIMIT: int | float


settings = Settings(
    DATE_FORMAT=os.getenv("DATE_FORMAT"),
    DB_URL=os.getenv("DB_URL"),
    TEST_DB_URL=os.getenv("TEST_DB_URL"),
    DEFAULT_CREDIT_LIMIT=os.getenv("DEFAULT_CREDIT_LIMIT"),
)
