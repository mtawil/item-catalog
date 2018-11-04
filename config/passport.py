from authomatic.providers import oauth2

SOCIAL_LOGIN = {
    'default': 'google',

    'google': {
        'class_': oauth2.Google,

        'consumer_key': '*************',
        'consumer_secret': '*************',

        'scope': oauth2.Google.user_info_scope,
        'url': 'https://www.googleapis.com/userinfo/v2/me',
    },
}
