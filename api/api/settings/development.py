# flake8: noqa

import os
import json

from .base import *

DEBUG = True

with open(os.path.join(BASE_DIR, 'secret.json')) as secret_file:
    secret = json.load(secret_file)
    SECRET_KEY = secret['dev']['SECRET_KEY']
    SOCIAL_AUTH_FACEBOOK_SECRET = secret['dev']['SOCIAL_AUTH_FACEBOOK_SECRET']
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = secret['dev']['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
    SOCIAL_AUTH_KAKAO_SECRET = secret['dev']['SOCIAL_AUTH_KAKAO_SECRET']
    SOCIAL_AUTH_NAVER_SECRET = secret['dev']['SOCIAL_AUTH_NAVER_SECRET']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CORS_ORIGIN_WHITELIST = [
    'localhost:3000',
    'dev.hycomputing.org',
]

ALLOWED_HOSTS = [
    'localhost',
    'dev.hycomputing.org',
    'devapi.hycomputing.org',
]

SOCIAL_AUTH_FACEBOOK_KEY = '188507875205839'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '618344253461-88t3aqni602h6ml4cgomrpedd58t03cl.apps.googleusercontent.com'

SOCIAL_AUTH_KAKAO_KEY = 'd35e08e945a4aa40e7c108811eb4aea3'

SOCIAL_AUTH_NAVER_KEY = 'AIZZ4ZfuMCi1Wx6jQQ7P'
