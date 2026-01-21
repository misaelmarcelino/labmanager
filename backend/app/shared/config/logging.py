import logging
from pathlib import Path
from datetime import datetime
from app.shared.config.base_dir import get_base_dir

BASE_DIR = get_base_dir()
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f"{datetime.now():%Y%m%d}_labmanager.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": str(log_file),
            "when": "midnight",
            "backupCount": 14,
            "formatter": "default",
            "encoding": "utf-8",
        },

    },

    # 🔴 ROOT LOGGER
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },

    # 🔴 UVICORN LOGGERS
    "loggers": {
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },

}
