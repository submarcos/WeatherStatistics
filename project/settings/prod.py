import os

from . import *  # NOQA

ALLOWED_HOSTS = [
    os.getenv("DOMAIN"),
]
DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    f"https://{os.getenv('DOMAIN')}",
]
