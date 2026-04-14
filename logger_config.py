"""
logger_config.py
================
Centralized logging configuration for Arachne.
Writes to both console (INFO+) and security_alerts.log (WARNING+).

Log format is structured for SIEM compatibility:
  TIMESTAMP | LEVEL | MESSAGE
"""

import logging
import sys
from pathlib import Path

LOG_FILE = Path("security_alerts.log")
LOG_FORMAT = "%(asctime)s UTC | %(levelname)-8s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_logger_initialized = False


def get_logger(name: str = "arachne") -> logging.Logger:
    """
    Returns the Arachne logger. Initializes it on first call.
    Subsequent calls return the same logger instance.
    """
    global _logger_initialized
    logger = logging.getLogger(name)

    if _logger_initialized:
        return logger

    logger.setLevel(logging.DEBUG)

    # ── Console handler (INFO and above) ─────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = _ColorFormatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    console_handler.setFormatter(console_formatter)

    # ── File handler (WARNING and above → security_alerts.log) ───────────────
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.WARNING)
    file_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    _logger_initialized = True
    return logger


class _ColorFormatter(logging.Formatter):
    """Adds ANSI color codes to console output."""

    COLORS = {
        logging.DEBUG:    "\033[90m",     # dark gray
        logging.INFO:     "\033[36m",     # cyan
        logging.WARNING:  "\033[33m",     # yellow
        logging.ERROR:    "\033[31m",     # red
        logging.CRITICAL: "\033[41;97m",  # red background, white text
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{self.RESET}"
