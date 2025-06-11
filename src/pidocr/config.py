"""Configuration utilities for pidocr."""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / '.env')

DATABASE_URL = os.getenv('DATABASE_URL', '')


def get_database_url() -> str:
    """Return the database connection URL from environment."""
    if not DATABASE_URL:
        raise ValueError('DATABASE_URL is not set in environment')
    return DATABASE_URL
