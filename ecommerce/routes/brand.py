from flask import Blueprint, jsonify, request, abort
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
    try:
        form = BrandForm(request.form)
        if form.validate():
            form.populate_obj(brand)
            brand.save()
            return jsonify(brand.to_dict()), 201
        else:
            response = {
                'status': 'fail',
                'errors': form.errors
            }
            raise Exception(response)
    except Exception as e:
        return jsonify(e.args[0]), 400


@brandBluePrint.route('/brand/<int:brand_id>', methods=['GET'])
def get_brand(brand_id):
    brand = Brand.query.get(brand_id)
    if brand is None:
        abort(404)
    return jsonify(brand.to_dict())


@brandBluePrint.route('/brand/<int:brand_id>', methods=['PATCH'])
def update_brand(brand_id):
    brand = Brand.query.get(brand_id)
    if brand is None:
        abort(404)
    try:
        form = BrandForm(request.form, partial=True)
        if form.validate():
            form.populate_obj(brand)
            brand.save()
            return jsonify(brand.to_dict()), 200
        else:
            response = {
                'status': 'fail',
                'errors': form.errors
            }
            raise Exception(response)
    except Exception as e:
        return jsonify(e.args[0]), 400


@brandBluePrint.route('/brand/<int:brand_id>', methods=['DELETE'])
def delete_brand(brand_id):
    brand = Brand.query.get(brand_id)
    if brand is None:
        abort(404)
    try:
        brand.delete()
        return jsonify({}), 204
    except Exception as e:
        return jsonify(e.args[0]), 400
