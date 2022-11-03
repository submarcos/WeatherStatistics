from . import *

ALLOWED_HOSTS = [
    os.getenv('DOMAIN'),
]
DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    os.getenv('DOMAIN'),
]