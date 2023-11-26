from functools import lru_cache
from typing import Union
from os import getenv
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, AnyUrl, EmailStr


class Settings(BaseSettings):
    # app config
    DEBUG: bool = getenv("DEBUG", True)
    APP_VERSION: str = getenv("APP_VERSION", "0.1.0")
    APP_NAME: str = getenv("APP_NAME", "FastAPI Starter")
    APP_DESCRIPTION: str = getenv("APP_DESCRIPTION", "A Starter FastAPI Project.")

    # Use this command to generate a SECRET_KEY: $ openssl rand -hex 32
    SECRET_KEY: str = getenv(
        "SECRET_KEY", "307003c8564ce849a858b6e9f8b0b2806744e9a06d040bbf1a945d5cf88a2aed"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    # DB Config
    DB_URI: Union[PostgresDsn, AnyUrl] = getenv("DB_URI", "sqlite:///./app.db")
    # email config
    SMTP_SERVER: str = getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = getenv("SMTP_PORT", 587)
    SMTP_USERNAME: EmailStr = getenv("SMTP_USERNAME", "parthjoshi90@gmail.com")
    SMTP_PASSWORD: str = getenv("SMTP_PASSWORD", "your_email_password")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
