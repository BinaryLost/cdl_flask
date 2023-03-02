from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, event
from ecommerce.app import db


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_added = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_added': self.date_added.isoformat(),
            'date_updated': self.date_updated.isoformat()
        }

    def __repr__(self):
        return f'<Brand {self.name}>'

    @staticmethod
    def get_all():
        return db.session.query(Brand).all()

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


@event.listens_for(Brand, 'before_update')
def receive_before_update(mapper, connection, target):
    target.date_updated = datetime.utcnow()
