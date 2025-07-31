from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    ALEMBIC_DB_URL: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    ACCESS_TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_DURATION: int
    ACCESS_TOKEN_ALGORITHM: str
    REFRESH_TOKEN_DURATION: int


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()