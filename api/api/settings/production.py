# flake8: noqa

import os
import json

from .base import *

DEBUG = False

with open(os.path.join(BASE_DIR, 'secret.json')) as secret_file:
    secret = json.load(secret_file)
    SECRET_KEY = secret['prod']['SECRET_KEY']

ALLOWED_HOSTS = [
    'api.hycomputing.org',
]
