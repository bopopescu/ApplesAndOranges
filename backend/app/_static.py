# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
from ._paths import *

STATIC_URL = '/_static/'

MEDIA_ROOT = os.path.join(BASE_DIR, '_media')
STATIC_ROOT = os.path.join(BASE_DIR, '_static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "assets"),
)

# for temporary upload files
FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, '_tmp')
