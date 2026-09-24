import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    mock_mode: bool = os.getenv("MOCK_MODE", "true").lower() == "true"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./astralab.db")
    llm_provider: str = os.getenv("LLM_PROVIDER", "mock")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://127.0.0.1:11434/v1")
    llm_model: str = os.getenv("LLM_MODEL", "qwen3:4b")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    literature_provider: str = os.getenv("LITERATURE_PROVIDER", "mock")
    experiment_timeout_seconds: int = int(os.getenv("EXPERIMENT_TIMEOUT_SECONDS", "60"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
