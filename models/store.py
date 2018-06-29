from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') #list of item models | including lazy makes creating faster but calls to json() slower

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]} #.all() with lazy='dynamic'

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # select * from users where name=name limit 1

    def save_to_db(self): #this method now inserts and updates
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()