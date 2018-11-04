import os

ORATOR_DATABASES = {
    'default': 'sqlite3',

    'sqlite3': {
        'driver': 'sqlite',
        'database': os.path.join(os.path.dirname(__file__), '../database.db')
    },

    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'database',
        'user': 'root',
        'password': '',
        'prefix': ''
    }
}
