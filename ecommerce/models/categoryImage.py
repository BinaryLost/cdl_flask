from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, event
from sqlalchemy.orm import relationship
from ecommerce.app import db


class CategoryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image = db.Column(db.LargeBinary, nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)

    category = relationship("Category", back_populates="image")
