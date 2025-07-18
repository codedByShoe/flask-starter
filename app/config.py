import os
from dotenv import load_dotenv


class Config:
    # Basic Flask configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "hard-to-guess-string")

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 25))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@example.com")
    VALKEY_URL = os.getenv("VALKEY_URL", "redis://localhost:6379/0")

    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "secure-salt")
    SECURITY_TOKEN_MAX_AGE = 3600  # 1 hour


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "hard-to-guess-string")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "secure-salt")
    SECURITY_TOKEN_MAX_AGE = 3600  # 1 hour


class DevelopmentConfig(BaseConfig):
    """
    Develoment configuration class that inherits from BaseConfig class.
    """

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.sqlite")
    # Mail configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 25))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@example.com")
    VALKEY_URL = os.getenv("VALKEY_URL", "redis://localhost:6379/0")


class ProductionConfig(BaseConfig):
    """
    Production configuration class that inherits from BaseConfig class.
    """

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.sqlite")
    # Mail configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 25))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@example.com")
    VALKEY_URL = os.getenv("VALKEY_URL", "redis://localhost:6379/0")
