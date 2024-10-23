"""
Configuration settings for the Online Classroom REST API.
Defines different configuration classes for various environments.
"""

import os
from datetime import timedelta
from cryptography.fernet import Fernet

def generate_key():
    """Generate a new Fernet key."""
    return Fernet.generate_key().decode()

class Config:
    """Base configuration class."""

    SECRET_KEY = os.getenv('SECRET_KEY', generate_key())
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Online Classroom REST API"
    API_VERSION = "v1"
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'classroom.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)

    def __repr__(self):
        return f"<Config {self.API_TITLE}, Version: {self.API_VERSION}>"

class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_ECHO = True

    def __repr__(self):
        return "<DevelopmentConfig>"

class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'

    def __repr__(self):
        return "<TestingConfig>"

class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False

    def __repr__(self):
        return "<ProductionConfig>"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
