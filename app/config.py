"""Application configuration and filesystem paths."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "records.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)
