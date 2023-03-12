from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, event
from sqlalchemy.orm import relationship
from ecommerce.app import db
import base64


class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    product = db.relationship("ProductBase", back_populates="images")
    image = db.Column(db.LargeBinary(length=(2 ** 20) * 10 - 1), nullable=False)
    mimetype = db.Column(db.String(50), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)

    def save(self):
        try:
            if self.id is None:
                db.session.add(self)
            db.session.commit()
        except Exception as e:
            raise Exception("Une erreur s'est produite lors de la sauvegarde : {}".format(str(e)))

    def delete(self):
        if self.product.active and len(self.product.images) == 1:
            raise Exception("Cannot delete the only image of an active product")
        db.session.delete(self)
        try:
            db.session.commit()
        except Exception as e:
            raise Exception("Une erreur s'est produite lors de la suppression : {}".format(str(e)))

    def to_dict(self):
        return {
            'id': self.id,
            'image': base64.b64encode(self.image).decode('utf-8') if self.image else None,
            'mimetype': self.mimetype,
        }

    # @staticmethod
    # def delete_product_image(category_id):
    #     category_image = CategoryImage.query.filter_by(category_id=category_id).first()
    #     if category_image:
    #         db.session.delete(category_image)
    #         db.session.commit()
