# flake8: noqa

import os

from .base import *

DEBUG = True

SECRET_KEY = '!h(!gt1k1pl)9kn#ull06iy2ybg$wj$uu%8)td$4*-_9!vw08v'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CORS_ORIGIN_WHITELIST = [
    'localhost:3000',
]

ALLOWED_HOSTS = [
    'localhost',
]
