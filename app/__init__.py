from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import redis
from rq import Queue

from config import get_config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

# Configure login manager
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"


def create_app(config_class=None):
    app = Flask(__name__)

    # Load configuration
    if config_class is None:
        app.config.from_object(get_config())
    else:
        app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Configure Redis and RQ
    app.redis = redis.from_url(app.config["VALKEY_URL"])
    app.task_queue = Queue("default", connection=app.redis)
    app.email_queue = Queue("email", connection=app.redis)

    # Import models to ensure they are registered with SQLAlchemy
    from app.auth.models import User

    # Register blueprints
    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.core import bp as core_bp

    app.register_blueprint(core_bp, url_prefix="")

    # Register error handlers
    from app.utils.error_handlers import register_error_handlers

    register_error_handlers(app)

    return app
