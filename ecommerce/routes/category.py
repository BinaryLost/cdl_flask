from flask import Blueprint, jsonify, request, abort
from ecommerce.config import AppConfig as config
from ecommerce.models.category import Category
from ecommerce.forms.category import CategoryFormCreate, CategoryFormEdit
from werkzeug.exceptions import BadRequest, NotFound
from ecommerce.errors import convert_form_errors_to_string
from http import HTTPStatus

categoryBluePrint = Blueprint('category', __name__)


@categoryBluePrint.route('/category', methods=['GET'])
def list_categories():
    try:
        categories = Category.query.all()
        return jsonify([category.to_dict() for category in categories])
    except Exception as e:
        raise e


@categoryBluePrint.route('/category', methods=['POST'])
def create_category():
    try:
        category = Category()
        form = CategoryFormCreate(request.form)
        if form.validate():
            form.populate_obj(category)
            category.save()
            return jsonify(category.to_dict()), HTTPStatus.CREATED
        else:
            raise BadRequest(convert_form_errors_to_string(form.errors))
    except Exception as e:
        raise e


@categoryBluePrint.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        category = Category.query.get(category_id)
        if category is None:
            raise NotFound()
        return jsonify(category.to_dict())
    except Exception as e:
        raise e


@categoryBluePrint.route('/category/<int:category_id>', methods=['PATCH'])
def update_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        raise NotFound()
    try:
        form = CategoryFormEdit(request.form, category=category)
        if form.validate():
            form.populate_obj(category)
            category.save()
            return jsonify(category.to_dict())
        else:
            raise BadRequest(convert_form_errors_to_string(form.errors))
    except Exception as e:
        raise e


@categoryBluePrint.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        raise NotFound()
    try:
        category.delete()
        return jsonify({}), HTTPStatus.NO_CONTENT
    except Exception as e:
        raise e
