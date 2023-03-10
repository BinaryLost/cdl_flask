from flask_wtf import FlaskForm
from wtforms import StringField, validators, IntegerField, BooleanField, FileField
from ecommerce.models.category import Category
from ecommerce.models.categoryImage import CategoryImage
from ecommerce.models.productFactory import ProductFactory


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
            if self.category.name not in ProductFactory.TYPES:
                raise validators.ValidationError(f'No final class {self.category.name} detected in the code')
        else:
            if self.category.has_products():
                raise validators.ValidationError('Must be final because has products.')

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
                'La cat??gorie parent s??lectionn??e ne doit pas ??tre un anc??tre de cette cat??gorie.')


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
        if not self.active.data and self.category.has_children(active=True):
            self.active.errors.append('Impossible because has ACTIVE children')
            return False
        if self.active.data and self.category.has_inactive_ancestors():
            self.active.errors.append('Parent categories must be active also')
            return False
        if not self.active.data and self.category.has_products(active=True):
            self.active.errors.append('Impossible because has ACTIVE products')
            return False
        return True
