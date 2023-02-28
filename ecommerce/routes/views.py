from flask import Blueprint

adminBluePrint = Blueprint('admin', __name__)


@adminBluePrint.route('/')
def index():
    return 'Hello from blueprint !'


@adminBluePrint.route('/about')
def about():
    return 'About blueprint'

