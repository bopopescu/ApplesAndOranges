# Djoser auth API configuration
from ._general import *
DJOSER = {
    'DOMAIN': DJANGO_SITE_DOMAIN,
    'SITE_NAME': DJANGO_SITE_NAME,
    'PASSWORD_RESET_CONFIRM_URL': '#/password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'LOGIN_AFTER_ACTIVATION': True,
    'LOGIN_AFTER_REGISTRATION': True,
    'SEND_ACTIVATION_EMAIL': False,
}

AUTH_RESET_CONFIRM_URL = 'https://{}/api/v1/auth/password/reset/confirm/'
AUTH_ACTIVATION_URL = 'https://{}/api/v1/auth/activate/'
