from flask import render_template
from flask_restful import Api

from app import app
from app.models.category import Category, CategoryAPI
from app.models.item import Item

api = Api(app)


@app.route('/')
@app.route('/catalog/')
def index():
    """
    Get all categories and latest items
    to be loaded to the homepage
    """

    # Get all categories
    categories = Category.all()

    # Get last 10 items ordering by its id
    latest_items = Item.with_('category').take(10).order_by('id', 'desc').get()

    return render_template(
        'index.html',
        categories=categories,
        latest_items=latest_items
    )


api.add_resource(CategoryAPI, '/catalog.json')


