import os
from dotenv import load_dotenv
load_dotenv()
from dataclasses import dataclass


@dataclass
class Settings:
    ai_api_key: str = os.getenv("AI_API_KEY", "")
    ai_base_url: str = os.getenv("AI_BASE_URL", "https://api.deepseek.com")
    ai_model: str = os.getenv("AI_MODEL", "deepseek-chat")
    scan_max_concurrency: int = int(os.getenv("SCAN_MAX_CONCURRENCY", "5"))
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    report_dir: str = "reports"

settings = Settings()
os.makedirs(settings.report_dir, exist_ok=True)