from flask import Flask
from config import Config
from .extensions import db, migrate, login_manager, mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    # Configure login manager
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

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
