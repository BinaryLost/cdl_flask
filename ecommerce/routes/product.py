from flask import Blueprint, jsonify, request, abort
from ecommerce.models.product import Shoes
from ecommerce.models.productImage import ProductImage
from werkzeug.exceptions import BadRequest, NotFound
from ecommerce.errors import convert_form_errors_to_string

productBluePrint = Blueprint('product', __name__)


@productBluePrint.route('/product', methods=['POST'])
def create_category():
    return "test"
    # try:
    #     category = Category()
    #     form = CategoryFormCreate(request.form)
    #     if form.validate():
    #         form.populate_obj(category)
    #         category.save()
    #         return jsonify(category.to_dict()), HTTPStatus.CREATED
    #     else:
    #         raise BadRequest(convert_form_errors_to_string(form.errors))
    # except Exception as e:
    #     raise e