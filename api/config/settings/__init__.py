import os

from django.core.exceptions import ImproperlyConfigured

ENV_DEVELOPMENT = 'development'
ENV_PRODUCTION = 'production'

APP_ENV = os.environ.get('APP_ENV', 'development')

if APP_ENV not in {ENV_DEVELOPMENT, ENV_PRODUCTION}:
    raise ImproperlyConfigured('Invalid APP_ENV setting.')

if APP_ENV == ENV_DEVELOPMENT:
    from .development import *
elif APP_ENV == ENV_PRODUCTION:
    from .production import *
