from flask import render_template, jsonify

from app import app
from app.models.category import Category
from app.models.item import Item


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


@app.route('/catalog.json')
def index_json():
    """
    Here is the JSON API Endpoints for getting
    all categories and related items
    """

    return jsonify({
        'categories': Category.with_('items').get().serialize()
    })
