"""Logging configuration for the trading bot."""

from __future__ import annotations

import logging
from pathlib import Path


LOG_FILE_NAME = "trading_bot.log"
LOGGER_NAME = "trading_bot"


def setup_logging() -> logging.Logger:
    """
    Configure and return the application logger.

    Logs are written to `trading_bot.log` in the project root.
    """
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    log_file_path = Path(LOG_FILE_NAME)
    # Ensure the log file exists as soon as logging is configured.
    log_file_path.touch(exist_ok=True)
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
