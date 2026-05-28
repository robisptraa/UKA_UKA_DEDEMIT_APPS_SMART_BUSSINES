import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    env: str = "development"
    project_name: str = "Uka-Uka AI Business OS"
    
    # Database
    database_url: str = "postgresql://postgres:secretpassword@localhost:5432/uka_uka_db"
    
    # Secrets
    jwt_secret: str = "super_secret_jwt_key_please_change_in_production_1234567890"
    access_token_expire_minutes: int = 1440
    
    # API Integrations
    anthropic_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    
    # Midtrans Indonesia Payments
    midtrans_server_key: Optional[str] = None
    midtrans_client_key: Optional[str] = None
    midtrans_is_production: bool = False
    
    # Telegram Bot
    telegram_bot_token: Optional[str] = None
    
    # Redis Cache & Storage
    redis_url: Optional[str] = "redis://localhost:6379/0"
    storage_bucket_url: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=[
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        ],
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
