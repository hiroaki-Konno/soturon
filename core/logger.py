import os
import sys

from loguru import logger

from settings import LOG_DIR, LOG_LEVEL


def setup_logger() -> None:
    """loguruのロガーを初期化する。run.py の起動時に一度だけ呼ぶ。"""
    logger.remove()

    logger.add(sys.stderr, level=LOG_LEVEL)

    os.makedirs(LOG_DIR, exist_ok=True)
    logger.add(
        os.path.join(LOG_DIR, "{time:YYYY-MM-DD}.log"),
        level="DEBUG",
        rotation="1 day",
        retention="30 days",
        encoding="utf-8",
    )
