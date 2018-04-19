from functools import wraps
from api.exceptions import AuthError

from django.utils.translation import gettext_lazy as _


def auth_required(func):
    @wraps(func)
    def wrap(info, *args, **kwargs):
        if not info.context.user.is_affiliation_authenticated:
            raise AuthError(message=_('affiliation authentication required'))
        return func(info, *args, **kwargs)
    return wrap
