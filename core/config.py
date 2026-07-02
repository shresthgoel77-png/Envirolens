import os
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Looks for .env file, but environment variables take precedence
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # App Settings
    APP_NAME: str = "SmartCity-PollutionBackend"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    # Infrastructure Settings
    DATABASE_URL: str = Field(
        ..., description="Async connection string for the database"
    )
    MODEL_PATH: str = Field(
        ..., description="Absolute path to the CV/ML model weights"
    )


# Instantiate to trigger validation immediately on import
settings = Settings()