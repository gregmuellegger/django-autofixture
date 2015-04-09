from django.contrib.auth.models import User
from django.test import TestCase
import autofixture


autofixture.autodiscover()


class AutodiscoverTestCase(TestCase):
    def test_builtin_fixtures(self):
        from autofixture.autofixtures import UserFixture
        self.assertEqual(autofixture.REGISTRY[User], UserFixture)
