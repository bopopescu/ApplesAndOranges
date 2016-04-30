"""
Django settings for iWinkit project.
For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# ----------------------------------------------------------------------------------------------
# General Django Configuration Starts Here
# ----------------------------------------------------------------------------------------------

from app._general import *
from app._paths import *
from app._installed_apps import *
from app._authentication import *
from app._internationalization import *
from app._middleware import *
from app._templates import *
from app._databases import *
from app._static import *
from app._logging import *
# storage configuration (aws s3 etc)

# email and sms notifications (twilio)

# PDF rendering default settings
from app._pdf import *
# cors headers exposed
from app._cors import *

# ----------------------------------------------------------------------------------------------
# Installed Django Apps Configuration Starts Here
# ----------------------------------------------------------------------------------------------

# Django Rest Framework (API Layer) Configuration
from app._drf import *
# Djoser API configuration
from app._djoser import *
# Django Suite Configuration (Admin replacement for Django Admin)
from app._admin import *
# Caching Framework (Cacheops)
from app._caching import *


# ----------------------------------------------------------------------------------------------
# Business Logic Custom Variables and Settings
# ----------------------------------------------------------------------------------------------
from app._business_logic import *

SITE_ID = 1
ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'

ADMINS = (
    ('Patrick Zhang', 'patdujour@gmail.com'),
)

MANAGERS = ADMINS

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# this is for tagging
TAGGIT_CASE_INSENSITIVE = True
