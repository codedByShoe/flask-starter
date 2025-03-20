import os
from datetime import timedelta


class Config:
    # Basic Flask configuration
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard-to-guess-string"

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "localhost"
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 1025)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "False").lower() in (
        "true",
        "yes",
        "1",
    )
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER") or "noreply@example.com"

    # Valkey/Redis configuration for RQ
    VALKEY_URL = os.environ.get("VALKEY_URL") or "redis://localhost:6379/0"

    # Security configuration
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") or "secure-salt"
    SECURITY_TOKEN_MAX_AGE = 3600  # 1 hour

    # RQ configuration
    RQ_REDIS_URL = VALKEY_URL
    RQ_QUEUES = ["default", "email", "high", "low"]


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    # Use stronger security settings for production
    SECURITY_TOKEN_MAX_AGE = 1800  # 30 minutes

    # Production should use HTTPS
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


# Configure based on environment
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config():
    return config[os.environ.get("FLASK_ENV", "default")]
