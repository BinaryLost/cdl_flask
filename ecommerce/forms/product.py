from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators
from ecommerce.models.productFactory import ProductFactory
from ecommerce.models.product import ProductBase as Product
from ecommerce.models.category import Category
from ecommerce.models.brand import Brand


class ProductFormCreate(FlaskForm):
    name = StringField('Name', [validators.DataRequired(),
                                validators.Length(min=2, max=80)])
    category_id = IntegerField('Category', [validators.DataRequired()])
    brand_id = IntegerField('Brand', [validators.DataRequired()])

    def validate_name(form, field):
        if Product.query.filter(Product.name.ilike(field.data)).first():
            raise validators.ValidationError('Name already exists.')

    def validate_category_id(form, field):
        category = Category.query.get(field.data)
        if category is None:
            raise validators.ValidationError('Invalid category')
        if not category.final:
            raise validators.ValidationError('Category must be final')
        if category.name.lower() not in ProductFactory.TYPES.keys():
            raise validators.ValidationError('Invalid product type.')

    def validate_brand_id(form, field):
        brand = Brand.query.get(field.data)
        if brand is None:
            raise validators.ValidationError('Invalid brand')
