from flask_wtf import FlaskForm
from wtforms import StringField, validators
from ecommerce.models.brand import Brand


class BrandForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired(),
                                validators.Length(min=2, max=80)])

    def validate_name(form, field):
        if Brand.query.filter(Brand.name.ilike(field.data)).first():
            raise validators.ValidationError('Name already exists.')
