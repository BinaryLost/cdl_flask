from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, event
from sqlalchemy.orm import relationship
from ecommerce.app import db
from .categoryImage import CategoryImage
from werkzeug.exceptions import BadRequest
import base64


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = db.Column(db.String(100), nullable=False)
    category_parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    final = db.Column(db.Boolean, default=False, nullable=False)
    active = db.Column(db.Boolean, default=False, nullable=False)
    image = relationship("CategoryImage", uselist=False, back_populates="category")

    category_children = relationship("Category",
                                     cascade="none",
                                     backref=db.backref('category_parent', remote_side=[id])
                                     )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'final': self.final,
            'active': self.active,
            'category_parent_id': self.category_parent_id,
            'ancestors': self.get_ancestors(),
            'image': self.image.to_dict() if self.image else None,
        }

    def __repr__(self):
        return f'<Category {self.name}>'

    @staticmethod
    def get_all():
        return db.session.query(Category).all()

    def save(self):
        if self.name:
            self.name = self.name.lower()
        try:
            if self.id is None:
                db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise Exception("Une erreur s'est produite lors de la sauvegarde : {}".format(str(e)))

    def delete(self):
        if self.has_children():
            raise BadRequest("La catégorie de ne doit pas être parent d'une autre catégorie")
        if self.has_products():
            raise BadRequest("Cannot be deleted because has products")
        CategoryImage.delete_category_image(self.id)
        db.session.delete(self)

        try:
            db.session.commit()
        except Exception as e:
            raise Exception("Une erreur s'est produite lors de la suppression : {}".format(str(e)))

    def get_ancestors(self):
        ancestors = []
        category = self
        while category.category_parent:
            category = category.category_parent
            ancestors.append({
                'id': category.id,
                'name': category.name,
                'final': category.final,
                'active': category.active,
                'category_parent_id': category.category_parent_id
            })
        return ancestors

    def has_inactive_ancestors(self):
        return any(not category['active'] for category in self.get_ancestors())

    def has_children(self, active=False):
        if active:
            return bool(Category.query.filter_by(category_parent_id=self.id, active=True).all())
        return bool(self.category_children)

    def has_products(self, active=False):
        if active:
            return any(product.active for product in self.products_in_category if product.active)
        else:
            return bool(self.products_in_category)

    @staticmethod
    def get_category_tree(category_id=None):
        categories = []
        if category_id is None:
            top_level_categories = Category.query.filter_by(category_parent_id=None).all()
        else:
            category = Category.query.get(category_id)
            if category is None:
                raise BadRequest("La catégorie donnée n'existe pas")
            top_level_categories = category.category_children

        for category in top_level_categories:
            category_dict = {
                'id': category.id,
                'name': category.name,
                'final': category.final,
                'active': category.active,
                'category_parent_id': category.category_parent_id
            }
            if category.has_children():
                category_dict['children'] = Category.get_category_tree(category.id)
            categories.append(category_dict)

        return categories
