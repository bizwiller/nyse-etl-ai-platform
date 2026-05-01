from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

DATA_DIR = BASE_DIR / "data"

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
