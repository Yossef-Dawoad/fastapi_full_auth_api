from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    database_url: str

    FRONTEND_HOST: str = 'http://localhost:3000'
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

class MailSettings(BaseSettings):

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    MAIL_FROM: str
    MAIL_FROM_NAME: str = 'auth-app'

    MAIL_DEBUG:bool
    USE_CREDENTIALS: bool # set true for prod

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_settings() -> Settings:
    return Settings()

mail_settings = MailSettings()
