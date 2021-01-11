import os
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).parent.absolute()

    TIMEOUT = 30

    # End points
    LOGIN_URL = "http://etest.bsmu.by/login/index.php"

    # Logs
    LOG_DIR = Path(os.environ.get("LOG_DIR", BASE_DIR / "../logs"))
    LOG_FILE_NAME = "etest_worker.log"
