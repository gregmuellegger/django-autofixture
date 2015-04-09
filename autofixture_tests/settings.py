import django
import os
import warnings


warnings.simplefilter('always')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite'),
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

SITE_ID = 1

# Set in order to catch timezone aware vs unaware comparisons
USE_TZ = True

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0'

ROOT_URLCONF = 'autofixture_tests.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',

    'autofixture',
    'autofixture_tests',
    'autofixture_tests.tests',
    'autofixture_tests.sample_app',
)

if django.VERSION >= (1, 7):
    INSTALLED_APPS = INSTALLED_APPS + (
        'autofixture_tests.appconfig_test.apps.AppConfigTestConfig',
    )

MIDDLEWARE_CLASSES = ()


if django.VERSION < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
else:
    TEST_RUNNER = 'django.test.runner.DiscoverRunner'
