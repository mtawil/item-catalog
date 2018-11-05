import os

db = {
    'default': 'sqlite',

    'sqlite': {
        'driver': 'sqlite',
        'database': os.path.join(os.path.dirname(__file__), '../database.db')
    },

    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'item_catalog',
        'user': 'root',
        'password': '',
    },

    'postgres': {
        'driver': 'postgres',
        'host': 'localhost',
        'database': 'item_catalog',
        'user': '',
        'password': '',
    }
}

ORATOR_DATABASES = {
    'development': db[db['default']]
}

