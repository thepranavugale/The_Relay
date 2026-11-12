
import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Project folders
DATA_DIR = BASE_DIR / "data"
PAPERS_DIR = DATA_DIR / "papers"
PROCESSED_DIR = DATA_DIR / "processed"

RESULTS_DIR = BASE_DIR / "results"
REPORTS_DIR = BASE_DIR / "reports"

# Groq configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "")
GROQ_BASE_URL = os.getenv(
    "GROQ_BASE_URL",
    "https://api.groq.com/openai/v1"
)

# Retry configuration
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))

REQUEST_TIMEOUT_SECONDS = int(
    os.getenv("REQUEST_TIMEOUT_SECONDS", "45")
)

# Create required folders
for folder in [
    PAPERS_DIR,
    PROCESSED_DIR,
    RESULTS_DIR,
    REPORTS_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)


def validate_config():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing in .env")

    if not GROQ_MODEL:
        raise ValueError("GROQ_MODEL is missing in .env")

    print("Configuration loaded successfully!")
    print("Groq Model:", GROQ_MODEL)


if __name__ == "__main__":
    validate_config()
