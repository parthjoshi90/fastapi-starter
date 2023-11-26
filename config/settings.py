from functools import lru_cache
from typing import Union
from os import getenv
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, AnyUrl, EmailStr

load_dotenv()


class Settings(BaseSettings):
    """
    Settings class for configuring the FastAPI application.

    Attributes:
        DEBUG (bool): Flag indicating whether the application is in debug mode.
        APP_VERSION (str): The version number of the FastAPI application.
        APP_NAME (str): The name of the FastAPI application.
        APP_DESCRIPTION (str): A brief description of the FastAPI application.
        SECRET_KEY (str): The secret key used for cryptographic operations.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Time duration for access token expiration in minutes.
        DB_URI (Union[PostgresDsn, AnyUrl]): Database URI for connecting to the database.
        SMTP_SERVER (str): SMTP server address for sending emails.
        SMTP_PORT (int): Port number for the SMTP server.
        SMTP_USERNAME (EmailStr): Username for authenticating with the SMTP server.
        SMTP_PASSWORD (str): Password for authenticating with the SMTP server.

    Note:
        The values for these attributes are loaded from environment variables. If an
        environment variable is not set, default values are used.

    Example:
        ```
        settings = Settings()
        print(settings.APP_NAME)
        ```
    """

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
    DB_URI: Union[PostgresDsn, AnyUrl] = getenv("DB_URI", "sqlite:///app.db")
    # email config
    SMTP_SERVER: str = getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = getenv("SMTP_PORT", 587)
    SMTP_USERNAME: EmailStr = getenv("SMTP_USERNAME", "parthjoshi90@gmail.com")
    SMTP_PASSWORD: str = getenv("SMTP_PASSWORD", "your_email_password")


@lru_cache
def get_settings() -> Settings:
    """
    Retrieve and return an instance of the Settings class.

    This function utilizes the LRU (Least Recently Used) caching mechanism to
    store and efficiently retrieve the settings. Subsequent calls to this function
    with the same parameters will return the cached result, avoiding the cost of
    recreating the Settings instance.

    Returns:
        Settings: An instance of the Settings class containing application configuration.
    """
    settings = Settings()
    return settings
