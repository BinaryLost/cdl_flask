from flask import Blueprint, jsonify, request
from ecommerce.config import AppConfig as config
from ecommerce.models.brand import Brand
from ecommerce.forms.brand import BrandForm

brandBluePrint = Blueprint('brand', __name__)


@brandBluePrint.route('/brand', methods=['GET'])
def list_brands():
    brands = Brand.query.all()
    return jsonify([brand.to_dict() for brand in brands])


@brandBluePrint.route('/brand', methods=['POST'])
def create_brand():
    form = BrandForm(request.form)
    if form.validate():
        brand = Brand(name=form.name.data)
        if brand.save():
            return jsonify(brand.to_dict()), 201
    errors = {
        'status': 'fail',
        'errors': form.errors
    }
    return jsonify(errors), 400


@brandBluePrint.route('/brand/<int:brand_id>', methods=['GET'])
def get_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    return jsonify(brand.to_dict())

@brandBluePrint.route('/brand/<int:brand_id>', methods=['PATCH'])
def update_brand(brand_id):
    brand = Brand.query.get(brand_id)
    if brand is None:
        response = {
            'status': 'error',
            'message': f'Brand with ID {brand_id} not found'
        }
        return jsonify(response), 404

    form = BrandForm(request.form, partial=True)
    if form.validate():
        form.populate_obj(brand)
        brand.save()
        return jsonify(brand.to_dict()), 200
    else:
        errors = {
            'status': 'fail',
            'errors': form.errors
        }
        return jsonify(errors), 400



@brandBluePrint.route('/brand/<int:brand_id>', methods=['DELETE'])
def delete_brand(brand_id):
    brand = Brand.query.get(brand_id)
    if brand is None:
        response = {
            'status': 'error',
            'message': f'Brand with ID {brand_id} not found'
        }
        return jsonify(response), 404

    brand.delete()

    response = {
        'brand': brand.to_dict()
    }
    return jsonify(response)


@brandBluePrint.route('/brand/<int:brand_id>/disable', methods=['POST'])
def disable_brand(brand_id):
    brand = Brand.query
    if brand is None:
        response = {
            'status': 'error',
            'message': f'Brand with ID {brand_id} not found'
        }
        return jsonify(response), 404

    brand.is_active = False
    brand.save()

    response = {
        'status': 'success',
        'data': {
            'brand': brand.to_dict()
        }
    }
    return jsonify(response)
