from django.contrib.auth.hashers import is_password_usable
from django.contrib.auth.models import User
from django.test import TestCase
import autofixture


autofixture.autodiscover()


class UserFixtureTest(TestCase):
    def test_discover(self):
        self.assertTrue(User in autofixture.REGISTRY)

    def test_basic(self):
        user = autofixture.create_one(User)
        self.assertTrue(user.username)
        self.assertFalse(is_password_usable(user.password))
