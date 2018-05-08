from django.utils.crypto import get_random_string


def make_token(
        chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
        length=50):
    return get_random_string(length, chars)
