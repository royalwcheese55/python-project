import os
from datetime import timedelta
from typing import Optional

from pydantic import BaseModel, Field


class Settings:
    def __init__(self) -> None:
        self.app_name: str = os.getenv("APP_NAME", "Store Locator Service")
        self.database_url: str = os.getenv("DATABASE_URL", "sqlite:///./store_locator.db")
        self.jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-me")
        self.jwt_algorithm: str = "HS256"
        self.access_token_exp_minutes: int = int(os.getenv("ACCESS_TOKEN_EXP_MINUTES", "15"))
        self.refresh_token_exp_days: int = int(os.getenv("REFRESH_TOKEN_EXP_DAYS", "7"))
        self.rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))
        self.rate_limit_per_hour: int = int(os.getenv("RATE_LIMIT_PER_HOUR", "100"))
        self.geocoding_user_agent: str = os.getenv("GEOCODING_USER_AGENT", "store-locator")
        self.enable_redis_cache: bool = os.getenv("ENABLE_REDIS_CACHE", "false").lower() == "true"
        self.redis_url: Optional[str] = os.getenv("REDIS_URL")


class TokenPayload(BaseModel):
    user_id: str
    email: str
    role: str
    exp: int


settings = Settings()


def access_token_timedelta() -> timedelta:
    return timedelta(minutes=settings.access_token_exp_minutes)


def refresh_token_timedelta() -> timedelta:
    return timedelta(days=settings.refresh_token_exp_days)
