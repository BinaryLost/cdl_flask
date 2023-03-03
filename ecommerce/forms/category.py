from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField, BooleanField
from ecommerce.models.category import Category


class CategoryFormCreate(FlaskForm):
    name = StringField('Name', [validators.DataRequired(),
                                validators.Length(min=2, max=80)])

    def validate_name(form, field):
        if Category.query.filter(Category.name.ilike(field.data)).first():
            raise validators.ValidationError('Name already exists.')


class CategoryFormEdit(FlaskForm):
    name = StringField('Nom', [validators.DataRequired(),
                               validators.Length(min=2, max=80)])
    category_parent_id = IntegerField('Parent', validators=[validators.Optional()])
    final = BooleanField('Final')
    active = BooleanField('Active')

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)
        super(CategoryFormEdit, self).__init__(*args, **kwargs)
        self.category = category

    def validate_category_parent_id(self, field):
        category_parent_id = field.data
        if category_parent_id == self.category.id:
            raise validators.ValidationError('Parent cannot be category itself')
        category_parent = Category.query.get(category_parent_id)
        if category_parent is None:
            raise validators.ValidationError('Category parent does not exist')
        if self.category.id in category_parent.get_ancestors():
            raise validators.ValidationError(
                'La catégorie parent sélectionnée ne doit pas être un ancêtre de cette catégorie.')
