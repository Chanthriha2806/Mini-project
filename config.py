import os

class Config:
    """Base configuration settings for the IT Infrastructure Monitoring Dashboard."""
    # Security keys
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345')
    TEMPLATES_AUTO_RELOAD = True
    
    # Database configuration
    # Default to SQLite for instant out-of-the-box execution.
    # To run on MySQL, set the DATABASE_URL environment variable or modify this string.
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'it_monitor_db')
    
    # Standard SQLite fallback (Use in-memory SQLite with StaticPool on Vercel)
    if os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV') or not os.access(os.path.abspath(os.path.dirname(__file__)), os.W_OK):
        from sqlalchemy.pool import StaticPool
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            'DATABASE_URL',
            'sqlite:///:memory:'
        )
        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {'check_same_thread': False},
            'poolclass': StaticPool
        }
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            'DATABASE_URL',
            f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'it_monitor_db.db')}"
        )
        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {
                'check_same_thread': False,
                'timeout': 30
            }
        }
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Flask-Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    # Monitor module threshold defaults (stored in db settings table eventually)
    DEFAULT_CPU_THRESHOLD = float(os.environ.get('DEFAULT_CPU_THRESHOLD', 90.0))
    DEFAULT_RAM_THRESHOLD = float(os.environ.get('DEFAULT_RAM_THRESHOLD', 90.0))
    DEFAULT_DISK_THRESHOLD = float(os.environ.get('DEFAULT_DISK_THRESHOLD', 95.0))
    DEFAULT_REFRESH_INTERVAL = int(os.environ.get('DEFAULT_REFRESH_INTERVAL', 5)) # in seconds
    DEFAULT_ALERT_EMAIL = os.environ.get('DEFAULT_ALERT_EMAIL', '')

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = False if (os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV')) else True

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    # In production, require strict environment values
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prod-secret-key-monitor-ai-2026-secure')

class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Export the config mapping
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

