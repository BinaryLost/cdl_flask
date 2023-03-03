from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, event
from sqlalchemy.orm import relationship
from ecommerce.app import db
from .categoryImage import CategoryImage


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
            'image_url': self.image.url if self.image else None,
            'category_parent_id': self.category_parent_id,
            'ancestors': self.get_ancestors()
        }

    def __repr__(self):
        return f'<Category {self.name}>'

    @staticmethod
    def get_all():
        return db.session.query(Category).all()

    def save(self):
        try:
            if self.id is None:
                db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise Exception("Une erreur s'est produite lors de la sauvegarde : {}".format(str(e)))

    def delete(self):
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
            ancestors.append(category.id)
        return ancestors


@event.listens_for(Category, 'before_update')
def receive_before_update(mapper, connection, target):
    target.date_updated = datetime.utcnow()
