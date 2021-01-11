import logging
from logging.handlers import RotatingFileHandler

from .config import Config


logger = logging.Logger(__name__)

Config.LOG_DIR.mkdir(exist_ok=True)
file_handler = RotatingFileHandler(
    str(Config.LOG_DIR / Config.LOG_FILE_NAME),
    maxBytes=1048576,
    backupCount=10,
)

file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s "
        "[in %(pathname)s:%(lineno)d]"
    )
)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
