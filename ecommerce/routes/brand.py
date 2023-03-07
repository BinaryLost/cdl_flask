from flask import Blueprint, jsonify, request, abort
from ecommerce.models.brand import Brand
from ecommerce.forms.brand import BrandForm
from werkzeug.exceptions import BadRequest, NotFound
from ecommerce.errors import convert_form_errors_to_string
from http import HTTPStatus

brandBluePrint = Blueprint('brand', __name__)


@brandBluePrint.route('/brand', methods=['GET'])
def list_brands():
    try:
        brands = Brand.get_all()
        return jsonify([brand.to_dict() for brand in brands])
    except Exception as e:
        raise e


@brandBluePrint.route('/brand', methods=['POST'])
def create_brand():
    try:
        brand = Brand()
        form = BrandForm(request.form)
        if form.validate():
            form.populate_obj(brand)
            brand.save()
            return jsonify(brand.to_dict()), HTTPStatus.CREATED
        else:
            raise BadRequest(convert_form_errors_to_string(form.errors))
    except Exception as e:
        raise e


@brandBluePrint.route('/brand/<int:brand_id>', methods=['GET'])
def get_brand(brand_id):
    try:
        brand = Brand.query.get(brand_id)
        if brand is None:
            raise NotFound()
        return jsonify(brand.to_dict())
    except Exception as e:
        raise e


@brandBluePrint.route('/brand/<int:brand_id>', methods=['PATCH'])
def update_brand(brand_id):
    brand = Brand.query.get(brand_id)
    if brand is None:
        raise NotFound()
    try:
        form = BrandForm(request.form)
        if form.validate():
            form.populate_obj(brand)
            brand.save()
            return jsonify(brand.to_dict())
        else:
            raise BadRequest(convert_form_errors_to_string(form.errors))
    except Exception as e:
        raise e


@brandBluePrint.route('/brand/<int:brand_id>', methods=['DELETE'])
def delete_brand(brand_id):
    brand = Brand.query.get(brand_id)
    if brand is None:
        raise NotFound()
    try:
        brand.delete()
        return jsonify({}), HTTPStatus.NO_CONTENT
    except Exception as e:
        raise e
