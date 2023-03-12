from flask import Blueprint, jsonify, request, abort
from ecommerce.models.category import Category
from ecommerce.models.categoryImage import CategoryImage
from ecommerce.forms.category import CategoryFormCreate, CategoryFormEdit, \
    CategoryParentFormEdit, CategoryFormActivate
from ecommerce.forms.categoryImage import CategoryImageAddForm, CategoryImageDeleteValidate, validate_image
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


@categoryBluePrint.route('/category/final', methods=['GET'])
def list_categories_final():
    try:
        categories = Category.query.filter(Category.final == True).all()
        return jsonify([category.to_dict() for category in categories])
    except Exception as e:
        raise e


@categoryBluePrint.route('/category/tree', methods=['GET'])
def list_category_tree():
    try:
        categories = Category.get_category_tree()
        return jsonify(categories)
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


@categoryBluePrint.route('/category/<int:category_id>/categoryparent', methods=['PATCH'])
def edit_category_parent(category_id):
    category = Category.query.get(category_id)
    if category is None:
        raise NotFound()
    try:
        form = CategoryParentFormEdit(request.form, category=category)
        if form.validate():
            form.populate_obj(category)
            category.save()
            return jsonify(category.to_dict())
        else:
            raise BadRequest(convert_form_errors_to_string(form.errors))
    except Exception as e:
        raise e


@categoryBluePrint.route('/category/<int:category_id>/activate', methods=['PATCH'])
def activate_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        raise NotFound()
    try:
        form = CategoryFormActivate(request.form, category=category)
        if form.validate():
            form.populate_obj(category)
            category.save()
            return jsonify(category.to_dict())
        else:
            raise BadRequest(convert_form_errors_to_string(form.errors))
    except Exception as e:
        raise e


@categoryBluePrint.route('/category/<int:category_id>/image', methods=['POST'])
def upload_category_image(category_id):
    try:
        category = Category.query.get(category_id)
        if category is None:
            raise NotFound()
        form = CategoryImageAddForm(request.form)
        if not form.validate():
            raise BadRequest(convert_form_errors_to_string(form.errors))
        is_valid, message = validate_image(request.files)
        if not is_valid:
            raise BadRequest(message)

        # Enregistrer l'image sur le serveur
        file = request.files['image']
        mimetype = file.mimetype
        image_data = file.read()
        image = CategoryImage(category_id=category_id, image=image_data, mimetype=mimetype)
        image.save()

        return jsonify(category.to_dict()), HTTPStatus.CREATED
    except Exception as e:
        raise e


@categoryBluePrint.route('/category/<int:category_id>/image', methods=['DELETE'])
def delete_category_image(category_id):
    try:
        category = Category.query.get(category_id)
        if category is None:
            raise BadRequest('La catégorie associée n\'existe pas')
        categoryImage = category.image
        if categoryImage is None:
            raise NotFound()
        print(category)

        is_valid, message = CategoryImageDeleteValidate.IsValidDeleteImage(category)
        if not is_valid:
            raise BadRequest(message)
        categoryImage.delete()
        return jsonify(category.to_dict()), HTTPStatus.CREATED
    except Exception as e:
        raise e
