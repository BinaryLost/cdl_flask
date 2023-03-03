from flask import Blueprint, jsonify, request, abort
from ecommerce.config import AppConfig as config
from ecommerce.models.category import Category
from ecommerce.forms.category import CategoryFormCreate, CategoryFormEdit

categoryBluePrint = Blueprint('category', __name__)


@categoryBluePrint.route('/category', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])


@categoryBluePrint.route('/category', methods=['POST'])
def create_category():
    try:
        category = Category()
        form = CategoryFormCreate(request.form)
        if form.validate():
            form.populate_obj(category)
            category.save()
            return jsonify(category.to_dict()), 201
        else:
            response = {
                'status': 'fail',
                'errors': form.errors
            }
            raise Exception(response)
    except Exception as e:
        return jsonify(e.args[0]), 400


@categoryBluePrint.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        abort(404)
    return jsonify(category.to_dict())


@categoryBluePrint.route('/category/<int:category_id>', methods=['PATCH'])
def update_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        abort(404)
    try:
        print(request.form)
        form = CategoryFormEdit(request.form, category=category)
        if form.validate():
            form.populate_obj(category)
            category.save()
            return jsonify(category.to_dict()), 200
        else:
            response = {
                'status': 'fail',
                'errors': form.errors
            }
            raise Exception(response)
    except Exception as e:
        return jsonify(e.args[0]), 400


@categoryBluePrint.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        abort(404)
    try:
        category.delete()
        return jsonify({}), 204
    except Exception as e:
        return jsonify(e.args[0]), 400
