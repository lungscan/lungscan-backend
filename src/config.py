import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    SUPPORTED_IMAGE_FORMATS = ["jpg", "jpeg", "png"]
    MODEL_VERSION = "densenet121-res224-all"
    PYTHONPATH = os.getenv("PYTHONPATH")


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    FLASK_ENV = "development"
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]

class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = "production"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")