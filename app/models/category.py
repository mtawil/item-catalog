from orator import mutator
from slugify import slugify
from app import db
from orator.orm import has_many


class Category(db.Model):
    __table__ = 'categories'
    __fillable__ = ['title']
    __hidden__ = ['slug']
    __timestamps__ = False

    @mutator
    def title(self, value):
        self.set_raw_attribute('title', value)
        self.set_raw_attribute('slug', slugify(value))

    @has_many
    def items(self):
        from app.models.item import Item

        return Item
