"""
CareerLens - Centralized Logging

Provides a reusable logger configuration for all Phase 2 modules.

Author: CareerLens
Python Version: 3.14
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import LOG_FILE, LOG_LEVEL

# Prevent configuring the logger multiple times
_LOGGER_INITIALIZED = False


def _create_formatter() -> logging.Formatter:
    """
    Create the standard log formatter.

    Returns:
        logging.Formatter
    """
    return logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)-8s | "
            "%(name)s | "
            "%(filename)s:%(lineno)d | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _create_console_handler() -> logging.StreamHandler:
    """
    Configure console logging.

    Returns:
        logging.StreamHandler
    """
    handler = logging.StreamHandler()
    handler.setFormatter(_create_formatter())
    return handler


def _create_file_handler() -> RotatingFileHandler:
    """
    Configure rotating log file.

    Returns:
        RotatingFileHandler
    """
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding="utf-8",
    )

    handler.setFormatter(_create_formatter())

    return handler


def _configure_root_logger() -> None:
    """
    Configure the root logger once.
    """
    global _LOGGER_INITIALIZED

    if _LOGGER_INITIALIZED:
        return

    root_logger = logging.getLogger()

    root_logger.setLevel(LOG_LEVEL)

    root_logger.addHandler(_create_console_handler())
    root_logger.addHandler(_create_file_handler())

    _LOGGER_INITIALIZED = True


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Args:
        name:
            Module name (__name__)

    Returns:
        logging.Logger
    """
    _configure_root_logger()

    return logging.getLogger(name)


if __name__ == "__main__":
    logger = get_logger(__name__)

    logger.debug("Debug message")
    logger.info("Logger initialized successfully.")
    logger.warning("Warning example.")
    logger.error("Error example.")
    logger.critical("Critical example.")
