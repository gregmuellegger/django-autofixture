from django.contrib.auth.models import User
from django.test import TestCase
import autofixture


class AutodiscoverTestCase(TestCase):
    def setUp(self):
        self.LOADING_ORIGINAL = autofixture.LOADING
        self.REGISTRY_ORIGINAL = autofixture.REGISTRY
        autofixture.LOADING = False
        autofixture.REGISTRY = {}

    def tearDown(self):
        autofixture.LOADING = self.LOADING_ORIGINAL
        autofixture.REGISTRY = self.REGISTRY_ORIGINAL


class BasicAutodiscoverTestCase(AutodiscoverTestCase):
    def test_builtin_fixtures(self):
        from autofixture.autofixtures import UserFixture
        autofixture.autodiscover()
        self.assertEqual(autofixture.REGISTRY, {
            User: UserFixture,
        })
