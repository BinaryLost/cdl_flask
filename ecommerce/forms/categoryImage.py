from flask_wtf import FlaskForm
from wtforms import validators, IntegerField
from ecommerce.models.categoryImage import CategoryImage
from io import BytesIO
from PIL import Image
from ecommerce.config import Config
from werkzeug.exceptions import BadRequest, NotFound


class CategoryImageAddForm(FlaskForm):
    category_id = IntegerField('category')

    def validate_category_id(form, field):
        category_image = CategoryImage.query.filter_by(category_id=field.data).first()
        if category_image:
            raise validators.ValidationError('La catégorie a déjà une image')


class CategoryImageDeleteValidate:

    @staticmethod
    def IsValidDeleteImage(category):
        if category.active:
            return False, 'Category must be inactive'
        return True, ''


def validate_image(files):
    try:
        if 'image' not in files:
            raise BadRequest('Le champ de formulaire "image" est manquant')

        file = files['image']
        if file.filename == '':
            raise BadRequest('Le champ de formulaire "image" est vide')

        img = Image.open(file)
        if img.format.lower() not in {'png', 'jpg', 'jpeg', 'gif'}:
            raise BadRequest('png', 'jpg', 'jpeg', 'gif')

        if file.content_length > Config.MAX_CONTENT_LENGTH:
            raise BadRequest('Taille d\'image trop grande')

        file.seek(0)
        return True, ''
    except Exception as e:
        return False, 'Erreur de validation d\'image : {}'.format(str(e))
