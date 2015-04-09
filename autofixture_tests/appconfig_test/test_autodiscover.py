import django
from django.conf import settings
from django.test import TestCase

import autofixture
from ..compat import skipIf
from .models import TestModel


class AutodiscoverTest(TestCase):
    @skipIf(django.VERSION < (1, 7), 'AppConfig only applies to Django >= 1.7')
    def test_testmodel_fixture_was_loaded(self):
        self.assertTrue(any(
            app for app in settings.INSTALLED_APPS
            if 'AppConfigTestConfig' in app))

        testmodelfixture = autofixture.REGISTRY[TestModel]
        self.assertEqual(testmodelfixture.__name__, 'CustomTestModelFixture')
