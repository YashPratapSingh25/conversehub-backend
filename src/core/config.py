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
    DEEPGRAM_API_KEY : str
    AZURE_SPEECH_KEY: str
    AZURE_SPEECH_REGION: str
    GEMINI_API_KEY : str
    ELEVENLABS_URL : str
    ELEVENLABS_API_KEY : str
    AZURE_STORAGE_ACCOUNT_NAME : str
    AZURE_STORAGE_ACCOUNT_KEY : str
    AZURE_BLOB_CONN_STRING : str
    INTERVIEW_AI_INTRO : str
    RESEND_API_KEY : str


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()