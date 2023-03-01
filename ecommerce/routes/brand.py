from flask import Blueprint, jsonify
from ecommerce.config import AppConfig as config
from ecommerce.models.brand import Brand


brandBluePrint = Blueprint('admin', __name__)


@brandBluePrint.route('/')
def index():
    return 'Hello from blueprint !'


@brandBluePrint.route('/brand', methods=['GET'])
def list_brands():
    brands = Brand.query.all()
    response = {
        'status': 'success',
        'data': {
            'brands': [brand.to_dict() for brand in brands]
        }
    }
    return jsonify(response)

