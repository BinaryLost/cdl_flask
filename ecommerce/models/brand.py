from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, event
from ecommerce.app import db


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Brand {self.name}>'

    @staticmethod
    def get_all():
        return db.session.query(Brand).all()


@event.listens_for(Brand, 'before_update')
def receive_before_update(mapper, connection, target):
    target.date_updated = datetime.utcnow()
