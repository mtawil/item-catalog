import hashlib
import uuid

from config import *

from flask import Flask, session, request, render_template
from flask_orator import Orator

""" Initialize the Flask app and load the templates """
app = Flask(__name__, template_folder='../resources/views', static_url_path='')

""" Load configurations """
app.config.from_object(__name__)

""" Set the secret app key """
app.secret_key = app.config['SECRET_KEY']

""" Start using the Orator ORM """
db = Orator(app)


""" ***************** CSRF Implementation ***************** """
""" I am not sure about where the below CSRF implementation """
""" should be placed. Should it be here or should be part of """
""" the controllers? Generally, I am getting it here because """
""" I think that the csrf is an important part of any web app """


def csrf_token():
    """
    Generate CSRF token and use it within templates

    :return: 512 bits of random string
    """

    if 'csrf_token' not in session:
        get_uuid = str(uuid.uuid4()).encode('utf-8')
        session['csrf_token'] = hashlib.sha512(get_uuid).hexdigest()

    return session.get('csrf_token')


app.jinja_env.globals.update(csrf_token=csrf_token)


@app.before_request
def csrf_protection():
    """
    Handling the CSRF protection when user send the post request
    """

    if request.method == 'POST':
        token = session.pop('csrf_token', None)

        # Simply throw to 403 page if the token is not exist, or not the same
        if not token or token != request.form.get('csrf_token'):
            return render_template('errors/403.html'), 403
