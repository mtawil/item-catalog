from orator import mutator
from slugify import slugify
from app import db
from orator.orm import belongs_to


class Item(db.Model):
    __table__ = 'items'
    __fillable__ = ['title', 'description']
    __hidden__ = ['slug']
    __timestamps__ = False

    @mutator
    def title(self, value):
        self.set_raw_attribute('title', value)
        self.set_raw_attribute('slug', slugify(value))

    @belongs_to
    def category(self):
        from app.models.category import Category

        return Category

    @belongs_to
    def user(self):
        from app.models.user import User

        return User
