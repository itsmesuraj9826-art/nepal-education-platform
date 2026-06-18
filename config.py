import os
from datetime import timedelta
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


def _db_uri():
    """
    Priority:
      1. DATABASE_URL env var (Render/Neon production — postgresql:// or postgres://)
      2. Individual DB_* vars → MySQL for local dev
    Uses URL.create() so special chars in passwords (e.g. @) are handled safely.
    """
    url = os.getenv('DATABASE_URL', '')
    if url:
        return url.replace('postgres://', 'postgresql://', 1)

    return URL.create(
        drivername='mysql+pymysql',
        username=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '3306')),
        database=os.getenv('DB_NAME', 'nepal_edu_platform'),
    )


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
