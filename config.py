import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB max request size
    CALCULATION_HISTORY_LIMIT = 100
    RATE_LIMIT_ENABLED = True


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'production'
    RATE_LIMIT_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    RATE_LIMIT_ENABLED = False


# Select config based on environment
config_name = os.getenv('FLASK_ENV', 'development')
if config_name == 'production':
    # Validate SECRET_KEY for production
    if not os.getenv('SECRET_KEY'):
        raise ValueError("SECRET_KEY environment variable must be set in production")
    config = ProductionConfig()
elif config_name == 'testing':
    config = TestingConfig()
else:
    config = DevelopmentConfig()
