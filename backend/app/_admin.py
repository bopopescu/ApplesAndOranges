# Django Suit Admin backend configuration
from ._general import *
SUIT_CONFIG = {
    # header
    'ADMIN_NAME': DJANGO_SITE_NAME,
    'HEADER_DATE_FORMAT': 'l, j. F Y',
    'HEADER_TIME_FORMAT': 'H:i',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'MENU_EXCLUDE': ('authtoken', 'auth'),
    'MENU': (
        {'app': 'auth', 'label': 'Authorization', 'icon': 'icon-lock'},
        {'app': 'users', 'label': 'Users', 'icon': 'icon-cog'},
    ),
    'MENU_OPEN_FIRST_CHILD': True,
}
