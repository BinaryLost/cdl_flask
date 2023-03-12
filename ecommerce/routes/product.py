from flask import Blueprint, jsonify, request, abort
from ecommerce.models.product import Shoes
from ecommerce.models.productImage import ProductImage
from werkzeug.exceptions import BadRequest, NotFound
from ecommerce.errors import convert_form_errors_to_string
from ecommerce.models.product import Shoes
from http import HTTPStatus

productBluePrint = Blueprint('product', __name__)


@productBluePrint.route('/product', methods=['POST'])
def create_category():
    try:
        # category = Category()
        # form = CategoryFormCreate(request.form)
        # if form.validate():
        #     form.populate_obj(category)
        #     category.save()
        #     return jsonify(category.to_dict()), HTTPStatus.CREATED
        # else:
        #     raise BadRequest(convert_form_errors_to_string(form.errors))
        new_shoe = Shoes(
            name="Ma nouvelle chaussure",
            description="Une chaussure de qualité supérieure",
            brand_id=1,
            price=50.0,
            category_id=16,
            shoe_size=42,
            shoe_type="Baskets",
            shoe_height="Montante",
            colors=["red", "white"]
        )
        new_shoe.save()
        return jsonify("dd"), HTTPStatus.CREATED
    except Exception as e:
        raise e