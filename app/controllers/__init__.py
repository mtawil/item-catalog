import glob
import os

from flask import send_from_directory, render_template
from flask import make_response, redirect, request, session, url_for
from flask_login import LoginManager, logout_user, login_required, login_user

from authomatic import Authomatic
from authomatic.adapters import WerkzeugAdapter
from orator.exceptions.orm import ModelNotFound

from app import app
from app.models.user import User


@app.errorhandler(404)
@app.errorhandler(ModelNotFound)
def page_not_found(e):
    """
    This is for handling 404 pages and it mostly
    comes when the app cannot find a Model, for
    example: Item.where('id', 1).first_or_fail()
    """

    return render_template('errors/404.html'), 404


""" Init Login Manager """
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized_access():
    """
    When a user trying to access unauthorized page
    """

    return render_template('errors/401.html'), 401


@login_manager.user_loader
def load_user(user_id):
    """
    Load the existing user to current_user variable

    :param user_id: The user id
    :return: User
    """

    return User.find(user_id)


@app.route('/login/<string:provider_name>')
def login_with(provider_name):
    """
    The below is login page action using OAuth with Google

    :param provider_name: The provider name. google by default
    """
    response = make_response()

    authomatic = Authomatic(app.config['SOCIAL_LOGIN'], app.secret_key)

    result = authomatic.login(
        WerkzeugAdapter(request, response),
        provider_name,
        None,
        session=session,
        session_saver=lambda: app.save_session(session, response)
    )

    if result and result.user and result.user.credentials:
        response = result.provider.access(
            authomatic.config.get(provider_name).get('url')
        )

        if response.status == 200:
            """
            Create a new user if the provided email is
            not exists. Otherwise, update the current user
            """
            user = User.first_or_new(email=response.data.get('email'))
            user.name = response.data.get('name')
            user.save()
            login_user(user)

        return redirect(url_for('index'))

    return response


@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('index'))


@app.route('/assets/<path:asset>')
def get_asset(asset):
    """
    The below is for loading the custom asset from
    (resources/assets) folder and send it to HTTP

    :param asset: the file path
    """

    return send_from_directory('../resources/assets', asset)


""" Load all controllers using the __all__ way """
__all__ = [
    os.path.basename(filename)[:-3]
    for filename in glob.glob(os.path.dirname(__file__) + "/*.py")
]
