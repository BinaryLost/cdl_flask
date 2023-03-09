from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, validators, IntegerField, BooleanField, FileField
from ecommerce.models.category import Category
from ecommerce.models.categoryImage import CategoryImage


class CategoryFormCreate(FlaskForm):
    name = StringField('Name', [validators.DataRequired(),
                                validators.Length(min=2, max=80)])

    def validate_name(form, field):
        if Category.query.filter(Category.name.ilike(field.data)).first():
            raise validators.ValidationError('Name already exists.')


class CategoryFormEdit(FlaskForm):
    name = StringField('Nom', [validators.DataRequired(),
                               validators.Length(min=2, max=80)])
    final = BooleanField('Final')
    active = BooleanField('Active')

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)
        super(CategoryFormEdit, self).__init__(*args, **kwargs)
        self.category = category

    def validate_name(self, field):
        category = Category.query.filter(Category.name.ilike(field.data)).first()
        if category and category.id != int(self.category.id):
            raise validators.ValidationError('Name already exists.')

    def validate_final(self, field):
        if field.data:
            if self.category.has_children():
                raise validators.ValidationError('Final category cannot have chidren.')

    def validate_active(self, field):
        if field.data:
            if not self.category.image and self.data:
                raise validators.ValidationError('Image obligatoire.')


class CategoryParentFormEdit(FlaskForm):
    category_parent_id = IntegerField('Parent', validators=[validators.Optional()])

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)
        super(CategoryParentFormEdit, self).__init__(*args, **kwargs)
        self.category = category

    def validate_category_parent_id(self, field):
        category_parent_id = field.data
        if category_parent_id == self.category.id:
            raise validators.ValidationError('Parent cannot be category itself')
        if category_parent_id == self.category.id:
            raise validators.ValidationError('Parent cannot be category itself')
        category_parent = Category.query.get(category_parent_id)
        if category_parent is None:
            raise validators.ValidationError('Category parent does not exist')
        if category_parent.final:
            raise validators.ValidationError('Category parent cannot be final')
        if self.category.id in category_parent.get_ancestors():
            raise validators.ValidationError(
                'La catégorie parent sélectionnée ne doit pas être un ancêtre de cette catégorie.')


class CategoryFormActivate(FlaskForm):
    active = BooleanField('Active')

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category', None)
        super(CategoryFormActivate, self).__init__(*args, **kwargs)

    def validate(self):
        if not super(CategoryFormActivate, self).validate():
            return False
        if not self.category.image and self.active.data:
            self.active.errors.append('Image is mandatory')
            return False
        return True

