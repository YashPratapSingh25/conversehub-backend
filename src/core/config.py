from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    ALEMBIC_DB_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()