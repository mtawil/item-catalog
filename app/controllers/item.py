from flask import render_template, request, redirect
from flask import url_for, current_app, flash
from flask_login import login_required, current_user
from orator.exceptions.orm import ModelNotFound
from slugify import slugify

from app import app
from app.models.category import Category
from app.models.item import Item


@app.route('/catalog/<string:category_slug>/')
@app.route('/catalog/<string:category_slug>/items/')
def list_items(category_slug):
    """
    Get all items of the current category

    :param category_slug:
    """

    # Get the category and check if it's exist or fail to 404 page if not
    category = Category.where('slug', category_slug).first_or_fail()

    return render_template(
        'items/index.html',
        category=category,
        items=category.items
    )


@app.route(
    '/catalog/<string:category_slug>/<string:item_slug>/',
    methods=['GET']
)
def view_item(category_slug, item_slug):
    """
    View the current item.

    :param category_slug: The category slug
    :param item_slug: The item slug
    """

    # Get the item and check if it's exist or fail to 404 page if not
    item = Item.where('slug', item_slug).first_or_fail()

    # Get the category slug from url and compare it with the item's
    # category slug, if both are not the same, redirect to the correct slug
    if category_slug != item.category.slug:
        return redirect(url_for(
            'view_item',
            category_slug=item.category.slug,
            item_slug=item.slug
        ))

    return render_template(
        'items/view.html',
        category=item.category,
        item=item
    )


@app.route('/catalog/add', methods=['GET'])
@app.route('/catalog/<string:category_slug>/add', methods=['GET'])
@login_required
def add_item(category_slug=None):
    """
    Add a new Item Form.

    :param category_slug: The category slug
    """

    # Get the current category using the slug
    current_category = Category.where('slug', category_slug).first()

    return render_template(
        'items/add.html',
        categories=Category.all(),
        current_category=current_category
    )


@app.route('/catalog/store', methods=['POST'])
@login_required
def store_item():
    """
    Store the new requested item.
    """

    # Get the category and check if it's exist or fail to 404 page if not
    category = Category.find_or_fail(request.form['category_id'])

    # Create new item
    item = Item()

    item.title = request.form['title']
    item.description = request.form['description']

    # Associate the new item with the category
    item.category().associate(category)

    # Associate the new item to the current user
    item.user().associate(current_user)

    # The below is for validate the unique slug, if it
    # was exists before, then the ORM will not fall to
    # the ModelNotFound exception and the code will
    # continue flashing the error message to the user.
    # Otherwise, if the slug is not exists, then the
    # request is completely valid and the ORM will
    # going to fall to the ModelNotFound exception
    # then save the new Item
    try:
        # Get the item and check if it's exist or fail to 404 page if not
        Item.where('slug', item.slug).first_or_fail()

        flash('The title seems similar to another'
              ' title, please choose another one.')

        return render_template(
            'items/add.html',
            categories=Category.all(),
            current_category=category,
            item=item

        )
    except ModelNotFound:
        # Save the item
        item.save()

    return redirect(url_for(
        'view_item',
        category_slug=category.slug,
        item_slug=item.slug
    ))


@app.route(
    '/catalog/<string:category_slug>/<string:item_slug>/edit',
    methods=['GET']
)
@login_required
def edit_item(category_slug, item_slug):
    """
    Edit the current item form.

    :param category_slug: The category slug
    :param item_slug: The item slug
    """

    # Get the item and check if it's exist or fail to 404 page if not
    item = Item.where('slug', item_slug).first_or_fail()

    # Make sure the current user is authorized or not
    if not item.user or item.user.id != current_user.id:
        return current_app.login_manager.unauthorized()

    # Get the category slug from url and compare it with the item's
    # category slug, if both are not the same, redirect to the correct slug
    if category_slug != item.category.slug:
        return redirect(url_for(
            'edit_item',
            category_slug=item.category.slug,
            item_slug=item.slug
        ))

    return render_template(
        'items/edit.html',
        categories=Category.all(),
        item=item
    )


@app.route('/catalog/update', methods=['POST'])
@login_required
def update_item():
    """
    Update the requested item.
    """

    # Get the category and check if it's exist or fail to 404 page if not
    category = Category.find_or_fail(request.form['category_id'])

    # Get the item and check if it's exist or fail to 404 page if not
    item = Item.find_or_fail(request.form['item_id'])

    # Make sure the current user is authorized or not
    if not item.user or item.user.id != current_user.id:
        return current_app.login_manager.unauthorized()

    # The below is for validate the unique slug, if it
    # was exists before, then the ORM will not fall to
    # the ModelNotFound exception and the code will
    # continue flashing the error message to the user.
    # Otherwise, if the slug is not exists, then the
    # request is completely valid and the ORM will
    # going to fall to the ModelNotFound exception
    # then save the new Item
    try:
        # Get the current item slug before it changing using ORM mutator
        old_item_slug = item.slug

        item.title = request.form['title']
        item.description = request.form['description']

        # Associate the new item with the category
        item.category().associate(category)

        # Associate the new item to the current user
        item.user().associate(current_user)

        # Get the item and check if it's exist or fail to 404 page if not
        Item.where('slug', item.slug).first_or_fail()

        # if the current slug is the same as requested then throw
        # to the ModelNotFound Exception and save the current item
        if item.slug == old_item_slug:
            raise ModelNotFound(item.__class__)

        flash('The title seems similar to another'
              ' title, please choose another one.')

        return render_template(
            'items/edit.html',
            categories=Category.all(),
            item=item
        )
    except ModelNotFound:
        # Save the item
        item.save()

    return redirect(url_for(
        'view_item',
        category_slug=category.slug,
        item_slug=item.slug
    ))


@app.route(
    '/catalog/<string:category_slug>/<string:item_slug>/delete',
    methods=['GET']
)
@login_required
def delete_item(category_slug, item_slug):
    """
    Confirm deleting the item.

    :param category_slug: The category slug
    :param item_slug: The item slug
    """

    # Get the item and check if it's exist or fail to 404 page if not
    item = Item.where('slug', item_slug).first_or_fail()

    # Make sure the current user is authorized or not
    if not item.user or item.user.id != current_user.id:
        return current_app.login_manager.unauthorized()

    # Get the category slug from url and compare it with the item's
    # category slug, if both are not the same, redirect to the correct slug
    if category_slug != item.category.slug:
        return redirect(url_for(
            'delete_item',
            category_slug=item.category.slug,
            item_slug=item.slug
        ))

    return render_template(
        'items/delete.html',
        item=item
    )


@app.route('/catalog/destroy', methods=['POST'])
@login_required
def destroy_item():
    """
    Delete the item.
    """

    # Get the item and check if it's exist or fail to 404 page if not
    item = Item.find_or_fail(request.form['item_id'])

    # Make sure the current user is authorized or not
    if not item.user or item.user.id != current_user.id:
        return current_app.login_manager.unauthorized()

    # Get the category slug before the item goes to delete
    category_slug = item.category.slug

    # Delete the item
    item.delete()

    return redirect(url_for(
        'list_items',
        category_slug=category_slug
    ))
