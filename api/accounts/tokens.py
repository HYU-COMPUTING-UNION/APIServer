from django.utils.crypto import get_random_string


def make_token(chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)',
               length=50):
    return get_random_string(length, chars)
