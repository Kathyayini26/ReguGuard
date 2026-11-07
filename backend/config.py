from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    PROJECT_NAME: str = "ReguGuard"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Vectorize Hindsight API Settings
    HINDSIGHT_API_KEY: Optional[str] = None
    HINDSIGHT_API_URL: str = "https://api.hindsight.vectorize.io"
    HINDSIGHT_BANK_ID: str = "reguguard-audit-bank"

    # Groq API Settings
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "qwen/qwen3-32b"

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()
