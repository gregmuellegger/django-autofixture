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
        self.assertTrue(len(user.username) <= 30)
        self.assertFalse(is_password_usable(user.password))

    def test_password_setting(self):
        user = autofixture.create_one(User, password='known')
        self.assertTrue(user.username)
        self.assertTrue(is_password_usable(user.password))
        self.assertTrue(user.check_password('known'))

        loaded_user = User.objects.get()
        self.assertEqual(loaded_user.password, user.password)
        self.assertTrue(loaded_user.check_password('known'))

#    def test_commit(self):
#        user = autofixture.create_one(User, commit=False)
#        self.assertEqual(user.pk, None)
