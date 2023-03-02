from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, event
from ecommerce.app import db


class ProductBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(DateTime, default=datetime.utcnow)
    date_updated = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.name}>'


class Product(ProductBase):
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)


class SubProduct(ProductBase):
    weight = db.Column(db.Float, nullable=False)
    size = db.Column(db.String(20), nullable=False)
