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
        "black": "Noir",
        "gray": "Gris",
        "white": "Blanc",
        "brown": "Marron",
        "beige": "Beige",
        "red": "Rouge",
        "pink": "Rose",
        "orange": "Orange",
        "yellow": "Jaune",
        "ecru": "Ecru",
        "green": "Vert",
        "turquoise": "Turquoise",
        "blue": "Bleu",
        "purple": "Violet",
        "gold": "Or",
        "silver": "Argent",
        "multicolor": "Multicolore",
        "transparent": "Transparent"
    }

    GENDER = {"man": "Homme", "woman": "Femme", "mixed": "Mixte"}
    SHOE_SIZE = [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45]
    SHOE_HEIGHT = {'high': 'Haute', 'low': 'Basse'}
    SHOE_TYPE = {'basket': 'Basket', 'low': 'Basse', 'mid': 'Mi-Haute'}


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    CORS_ORIGINS = ['http://localhost:5173']
    CORS_HEADERS = ['Content-Type', 'Access-Control-Allow-Origin']
    CORS_SUPPORTS_CREDENTIALS = True


class TestingConfig(Config):
    pass
