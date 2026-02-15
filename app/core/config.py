from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_ENV: str = "development"
    API_KEY: str = "admin-secret-key"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///./incidents.db"
    RISK_THRESHOLD: int = 50

    class Config:
        env_file = ".env"

settings = Settings()
