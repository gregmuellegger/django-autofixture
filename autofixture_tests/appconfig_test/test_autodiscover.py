from django.conf import settings
from django.test import TestCase

import autofixture
from .models import TestModel


class AutodiscoverTest(TestCase):
    def test_testmodel_fixture_was_loaded(self):
        self.assertTrue(any(
            app for app in settings.INSTALLED_APPS
            if 'AppConfigTestConfig' in app))

        testmodelfixture = autofixture.REGISTRY[TestModel]
        self.assertEqual(testmodelfixture.__name__, 'CustomTestModelFixture')
