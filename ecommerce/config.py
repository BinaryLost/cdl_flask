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
    COLOR_CHOICES = {
        "red": "Rouge",
        "blue": "Bleu",
        "green": "Vert",
        "black": "Noir",
        "white": "Blanc",
        "yellow": "Jaune",
        "purple": "Violet",
        "gray": "Gris",
        "brown": "Marron",
    },
    SHOE_SIZE = [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    CORS_ORIGINS = ['http://localhost:5173']
    CORS_HEADERS = ['Content-Type', 'Access-Control-Allow-Origin']
    CORS_SUPPORTS_CREDENTIALS = True


class TestingConfig(Config):
    pass
