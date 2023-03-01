import os


class AppConfig:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://hag:hagisgood@localhost/cdl'
    CORS_ORIGINS = ['http://localhost:5173']
