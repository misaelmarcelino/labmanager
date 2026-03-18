import logging
from pathlib import Path
from datetime import datetime


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f"{datetime.now():%Y%m%d}_standinauto.log"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("standinauto")