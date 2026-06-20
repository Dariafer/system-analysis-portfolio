from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Payment Gateway API"
    app_version: str = "1.0.0"
    app_env: str = "local"

    api_v1_prefix: str = "/api/v1"

    default_merchant_api_key: str = "test-api-key"

    database_url: str = (
        "postgresql+asyncpg://payment_user:payment_password"
        "@localhost:5432/payment_gateway"
    )

    webhook_retry_attempts: int = 3
    webhook_retry_interval_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
