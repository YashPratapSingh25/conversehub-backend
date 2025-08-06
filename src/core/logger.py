from loguru import logger
from pathlib import Path
from sys import stdout

Path("logs").mkdir(exist_ok=True)

logger.remove()

logger.add(
    stdout,
    level="DEBUG",
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    ),
    enqueue=False
)

logger.add(
    "logs/backend.log",
    level="INFO",
    rotation="1 MB",
    compression=".zip",
    enqueue=False,
    serialize=True
)