import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://hag:hagisgood@localhost/cdl'
    WTF_CSRF_ENABLED = False
    UPLOADED_IMAGES_DEST = 'static/img/'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    IMAGES_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    CORS_ORIGINS = ['http://localhost:5173']
    CORS_HEADERS = ['Content-Type', 'Access-Control-Allow-Origin']
    CORS_SUPPORTS_CREDENTIALS = True

class TestingConfig(Config):
    pass

