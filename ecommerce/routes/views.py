from flask import Blueprint
from ecommerce.config import AppConfig as config
from ecommerce.models.brand import Brand


adminBluePrint = Blueprint('admin', __name__)


@adminBluePrint.route('/')
def index():
    return 'Hello from blueprint !'


@adminBluePrint.route('/about')
def about():
    return 'About blueprint'


@adminBluePrint.route('/key')
def key():
    return config.BASE_DIR
