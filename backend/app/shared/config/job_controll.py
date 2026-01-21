from pathlib import Path
from datetime import date
from app.shared.config.base_dir import get_base_dir
import sys

LOG_DIR = get_base_dir() / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = LOG_DIR / "last_equipment_job.txt"

def already_ran_today() -> bool:
    if not STATE_FILE.exists():
        return False
    return STATE_FILE.read_text().strip() == date.today().isoformat()

def mark_as_ran_today():
    STATE_FILE.write_text(date.today().isoformat())
