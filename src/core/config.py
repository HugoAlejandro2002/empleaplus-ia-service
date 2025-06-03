from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model: str
    openai_api_key: str

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "us-east-1"
    dynamodb_skills_table: str
    dynamodb_users_table: str
    dynamodb_resumes_table: str

    jwt_secret_key: str
    jwt_hash_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30


    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()
