from app import db
from orator.orm import has_many


class User(db.Model):
    __table__ = 'users'
    __fillable__ = ['email', 'name']
    __timestamps__ = False

    @has_many
    def items(self):
        from app.models.item import Item

        return Item

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.get_attribute('id')
