from django.contrib.auth.hashers import is_password_usable
from django.contrib.auth.models import User
import autofixture
from .autodiscover import AutodiscoverTestCase


class UserFixtureTest(AutodiscoverTestCase):
    def test_basic(self):
        autofixture.autodiscover()

        user = autofixture.create_one(User)

        self.assertTrue(user.username)
        self.assertFalse(is_password_usable(user.password))
