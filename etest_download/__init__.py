import logging
from logging.handlers import RotatingFileHandler
from typing import Type

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
moment = Moment()
migrate = Migrate()


def create_app(config_class: Type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)

    login_manager.anonymous_user.email = "<anonymous>"
    login_manager.login_view = "auth.login"

    app.config["FILES_DIR"].mkdir(parents=True, exist_ok=True)

    from etest_download.main import bp as main_bp
    app.register_blueprint(main_bp)

    from etest_download.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from etest_download.files import bp as download_bp
    app.register_blueprint(download_bp)

    app.config["LOG_DIR"].mkdir(exist_ok=True)
    file_handler = RotatingFileHandler(
        str(app.config["LOG_DIR"] / app.config["LOG_FILE_NAME"]),
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
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("E-Test Download Tool Startup")

    return app
