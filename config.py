import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def _db_uri():
    """
    Priority:
      1. DATABASE_URL  (Vercel Postgres sets this automatically)
      2. Individual DB_HOST/USER/PASS vars (local dev / Docker)
    Vercel Postgres gives a postgres:// URI — SQLAlchemy needs postgresql://
    """
    url = os.getenv('DATABASE_URL', '')
    if url:
        # Vercel uses 'postgres://' — SQLAlchemy needs 'postgresql://'
        return url.replace('postgres://', 'postgresql://', 1)

    host     = os.getenv('DB_HOST', 'localhost')
    port     = os.getenv('DB_PORT', '5432')
    name     = os.getenv('DB_NAME', 'nepal_edu_platform')
    user     = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', '')
    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-change-me')
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = _db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_pre_ping': True,
        'pool_size': 5,
        'max_overflow': 2,
    }

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-dev-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    AI_PROVIDER  = os.getenv('AI_PROVIDER', 'openai')
    OPENAI_API_KEY  = os.getenv('OPENAI_API_KEY', '')
    GEMINI_API_KEY  = os.getenv('GEMINI_API_KEY', '')

    REDIS_URL = os.getenv('REDIS_URL', '')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', '')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', '')

    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/tmp/uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    ALLOWED_DOC_EXTENSIONS = {'pdf', 'doc', 'docx'}
    STORAGE_BACKEND = os.getenv('STORAGE_BACKEND', 'local')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET', '')

    TESSERACT_CMD = os.getenv('TESSERACT_CMD', '/usr/bin/tesseract')

    EMIS_API_URL = os.getenv('EMIS_API_URL', '')
    EMIS_API_KEY = os.getenv('EMIS_API_KEY', '')
    SYNC_INTERVAL_HOURS = int(os.getenv('SYNC_INTERVAL_HOURS', 24))

    MAIL_SERVER   = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT     = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS  = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')

    ITEMS_PER_PAGE = 25


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config_map = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
    'testing':     TestingConfig,
    'default':     DevelopmentConfig,
}
