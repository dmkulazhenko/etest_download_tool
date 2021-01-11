import os
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).parent.absolute()

    # Logs
    LOG_DIR = Path(os.environ.get("LOG_DIR", BASE_DIR / "../logs"))
    LOG_FILE_NAME = "etest_download_tool.log"

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(BASE_DIR / "edt.db")

    MYSQL_CREDENTIALS = (
        os.environ.get("MYSQL_CONNECTOR"),
        os.environ.get("MYSQL_USER"),
        os.environ.get("MYSQL_PASSWORD"),
        os.environ.get("MYSQL_HOST"),
        os.environ.get("MYSQL_DATABASE"),
    )
    if all(MYSQL_CREDENTIALS):
        SQLALCHEMY_DATABASE_URI = "mysql+{}://{}:{}@{}/{}".format(
            *MYSQL_CREDENTIALS
        )

    SQLALCHEMY_MIGRATIONS_DIR = (
        os.environ.get("SQLALCHEMY_MIGRATIONS_DIR") or "migrations"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Keys
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Files
    FILES_DIR_NAME = "files"
    FILES_DIR = Path(
        os.environ.get("FILES_DIR", BASE_DIR / "static" / FILES_DIR_NAME)
    )
