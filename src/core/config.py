from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model: str
    openai_api_key: str

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "us-east-1"
    dynamodb_table_name: str


    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()
