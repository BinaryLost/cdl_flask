import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from ecommerce.models.category import Category
from ecommerce.models.brand import Brand

from ecommerce.app import db

COLOR_CHOICES = {
    "red": "Rouge",
    "blue": "Bleu",
    "green": "Vert",
    "black": "Noir",
    "white": "Blanc",
    "yellow": "Jaune",
    "purple": "Violet",
    "gray": "Gris",
    "brown": "Marron",
}

accessories_table = db.Table('accessories',
                             db.Column('parent_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
                             db.Column('accessory_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
                             )


class ProductBase(db.Model):

    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    name = Column(String(255))
    description = Column(Text)
    brand_id = Column(Integer, ForeignKey(Brand.id))
    brand = relationship("Brand")
    price = Column(Float)
    is_accessory = Column(Boolean, default=False)
    accessories = relationship(
        'ProductBase',
        secondary=accessories_table,
        primaryjoin=id == accessories_table.c.parent_id,
        secondaryjoin=id == accessories_table.c.accessory_id,
        back_populates='accessory_of'
    )

    accessory_of = relationship(
        'ProductBase',
        secondary=accessories_table,
        primaryjoin=id == accessories_table.c.accessory_id,
        secondaryjoin=id == accessories_table.c.parent_id,
        back_populates='accessories'
    )
    category_id = Column(Integer, ForeignKey(Category.id))
    category = relationship("Category")
    active = Column(Boolean, default=True)
    images = relationship("ProductImage", back_populates="product")
    attributes = Column(JSON)

    __mapper_args__ = {
        "polymorphic_on": attributes["type"],
        "polymorphic_identity": "product"
    }

    def __init__(self, **kwargs):
        self.attributes = {
            "shoe_size": None,
            "shoe_type": None,
            "shoe_height": None,
            "colors": []
        }
        super().__init__(**kwargs)

    @property
    def attributes_dict(self):
        return self.attributes

    def add_accessory(self, accessory):
        if accessory not in self.accessories:
            self.accessories.append(accessory)

    def remove_accessory(self, accessory):
        if accessory in self.accessories:
            self.accessories.remove(accessory)


class Shoes(ProductBase):
    __mapper_args__ = {
        "polymorphic_identity": "shoe"
    }

    def __init__(self, **kwargs):
        self.attributes.update({
            "shoe_size": None,
            "shoe_type": None,
            "shoe_height": None,
            "colors": []
        })
        super().__init__(**kwargs)

    @property
    def attributes_dict(self):
        return {
            "shoe_size": self.attributes["shoe_size"],
            "shoe_type": self.attributes["shoe_type"],
            "shoe_height": self.attributes["shoe_height"],
            "colors": [COLOR_CHOICES[color_key] for color_key in self.attributes["colors"]]
        }
