import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from ecommerce.models.category import Category
from ecommerce.models.productImage import ProductImage
from ecommerce.models.brand import Brand
from sqlalchemy.orm import mapper
from ecommerce.config import Config

from ecommerce.app import db

COLOR_CHOICES = Config.COLOR_CHOICES
GENDER = Config.GENDER

accessories_table = db.Table('accessories',
                             db.Column('parent_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
                             db.Column('accessory_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
                             )


class ProductBase(db.Model):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    date_added = Column(DateTime, default=datetime.datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    active = Column(Boolean, default=False, nullable=False)
    name = Column(String(255), nullable=False)
    gender = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    brand_id = Column(Integer, ForeignKey(Brand.id))
    brand = relationship("Brand")
    price = Column(Float, default=0, nullable=False)
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
    images = relationship("ProductImage", back_populates="product")
    attributes = Column(JSON)
    # type = Column(String(50))

    # __mapper_args__ = {
    #     "polymorphic_on": "type",
    #     "polymorphic_identity": None
    # }

    def __init__(self, **kwargs):
        self.type = kwargs.pop("type", None)
        self.attributes = kwargs.pop("attributes", {})
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'date_added': self.date_added,
            'date_updated': self.date_updated,
            'name': self.name,
            'description': self.description,
            'brand': self.brand.name,
            'gender': Config.GENDER[self.gender],
            'price': self.price,
            'is_accessory': self.is_accessory,
            'accessories': [accessory.to_dict() for accessory in self.accessories],
            'category': self.category.name,
            'active': self.active,
            'images': [image.to_dict() for image in self.images],
        }

    def add_accessory(self, accessory):
        if accessory not in self.accessories:
            self.accessories.append(accessory)

    def remove_accessory(self, accessory):
        if accessory in self.accessories:
            self.accessories.remove(accessory)

    def save(self):
        try:
            self.update_attributes()
            if self.id is None:
                db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise Exception("Une erreur s'est produite lors de la sauvegarde : {}".format(str(e)))


class Shoe(ProductBase):
    # __mapper_args__ = {
    #     "polymorphic_identity": "shoe"
    # }

    def __init__(self, shoe_size=None, shoe_type=None, shoe_height=None, colors=None, **kwargs):
        # kwargs["type"] = self.__mapper_args__["polymorphic_identity"]
        self.shoe_size = shoe_size
        self.shoe_type = shoe_type
        self.shoe_height = shoe_height
        self.colors = colors or []
        super().__init__(**kwargs)

    def to_dict(self):
        base_dict = super().to_dict()
        attributes_dict = {
            "shoe_size": self.attributes["shoe_size"],
            "shoe_type": Config.SHOE_TYPE[self.attributes["shoe_type"]],
            "shoe_height": Config.SHOE_HEIGHT[self.attributes["shoe_height"]],
            "colors": [COLOR_CHOICES[color_key] for color_key in self.attributes["colors"]]
        }
        base_dict["attributes"] = attributes_dict
        return base_dict

    def update_attributes(self):
        self.attributes.update({
            "shoe_size": self.shoe_size,
            "shoe_type": self.shoe_type,
            "shoe_height": self.shoe_height,
            "colors": self.colors
        })
