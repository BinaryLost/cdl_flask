from flask import Blueprint, jsonify, request, abort
from werkzeug.exceptions import BadRequest, NotFound
from ecommerce.errors import convert_form_errors_to_string
from ecommerce.models.product import ProductBase
from ecommerce.models.productImage import ProductImage
from ecommerce.models.product import Shoe
from ecommerce.models.productFactory import ProductFactory
from ecommerce.models.category import Category
from ecommerce.forms.product import ProductFormCreate
from http import HTTPStatus

productBluePrint = Blueprint('product', __name__)


@productBluePrint.route('/product', methods=['GET'])
def list_products():
    try:
        products = ProductBase.query.all()
        return jsonify([product.to_dict() for product in products])
    except Exception as e:
        raise e


@productBluePrint.route('/product', methods=['POST'])
def create_product():
    try:
        category = Category.query.get(request.form.get('category_id'))
        if category is None:
            raise BadRequest('Invalid category')
        form = ProductFormCreate(request.form)
        if form.validate():
            product_factory = ProductFactory()
            product_factory.set_product_class(category.name)
            product = product_factory.create_product()
            form.populate_obj(product)
            product.save()
            return jsonify(product_class.to_dict()), HTTPStatus.CREATED
        else:
            raise BadRequest(convert_form_errors_to_string(form.errors))
        # type_product = "shoe"
        # product_class = ProductFactory.TYPES.get(type_product)
        # if product_class is None:
        #     raise BadRequest(f"Type de produit inconnu: {type_product}")
        # new_shoe = product_class(
        #     name="Ma nouvelle NIKE",
        #     description="Une chaussure de qualité supérieure",
        #     brand_id=1,
        #     price=100.0,
        #     gender="man",
        #     category_id=1,
        #     shoe_size=44,
        #     shoe_type="basket",
        #     shoe_height="high",
        #     colors=["red", "white"]
        # )
        # new_shoe.save()
        return jsonify("dd"), HTTPStatus.CREATED
    except Exception as e:
        raise e
