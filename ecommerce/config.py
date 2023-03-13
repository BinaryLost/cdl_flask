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
    SHOE_SIZE = [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]
    SHOE_HEIGHT = {'high': 'Haute', 'low': 'Basse'}
    SHOE_TYPE = {'sneaker': 'Sneaker', 'shoe': 'Chaussure', 'sandal': 'Sandale'}
    JEAN_SIZE = [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
    LETTER_SIZE = ['S', 'M', 'L', 'XL', 'XXL']


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    CORS_ORIGINS = ['http://localhost:5173']
    CORS_HEADERS = ['Content-Type', 'Access-Control-Allow-Origin']
    CORS_SUPPORTS_CREDENTIALS = True


class TestingConfig(Config):
    pass
