from django.contrib.gis.geos import Point
from django.test.utils import override_settings

from autofixture import generators
from . import FileSystemCleanupTestCase


class GeoDjangoPointTests(FileSystemCleanupTestCase):

    @override_settings(INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',
        'django.contrib.gis',

        'autofixture',
        'autofixture_tests',
        'autofixture_tests.tests',
        'autofixture_tests.sample_app',
    ))
    def test_point(self):

        point = generators.PointFieldGenerator().generate()
        self.assertIsInstance(point, Point)
