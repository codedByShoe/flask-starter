import os
from dotenv import load_dotenv
from flask import Flask
from .extensions import db, migrate, login_manager, mail


class Application:
    CONFIG_MAP = {
        "development": "app.config.DevelopmentConfig",
        "production": "app.config.ProductionConfig",
        "testing": "app.config.TestingConfig",
    }

    @property
    def app(self) -> Flask:
        return self._app

    @app.setter
    def app(self, app: Flask) -> None:
        self._app = app

    def __init__(self) -> None:
        self.app = Flask(__name__)
        load_dotenv()
        self._load_config()

    def _load_config(self) -> None:
        env = os.getenv("FLASK_ENV", "development")

        config_class = self.CONFIG_MAP.get(env, "app.config.DevelopmentConfig")
        self.app.config.from_object(config_class)

    def add_extensions(self):
        db.init_app(self.app)
        migrate.init_app(self.app, db)
        login_manager.init_app(self.app)
        mail.init_app(self.app)

        # Configure login manager
        login_manager.login_view = "auth.login"
        login_manager.login_message = "Please log in to access this page."
        login_manager.login_message_category = "info"

        return self

    def build(self) -> Flask:
        return self.app
