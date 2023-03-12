from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators
from ecommerce.models.productFactory import ProductFactory
from ecommerce.models.product import ProductBase as Product
from ecommerce.models.category import Category


class ProductFormCreate(FlaskForm):
    name = StringField('Name', [validators.DataRequired(),
                                validators.Length(min=2, max=80)])
    category_id = IntegerField('Category', [validators.DataRequired()])

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
