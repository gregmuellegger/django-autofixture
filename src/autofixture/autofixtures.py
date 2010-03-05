# -*- coding: utf-8 -*-
import autofixture
import string
from datetime import datetime
from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from autofixture import AutoFixture
from autofixture import generators


class UserFixture(AutoFixture):
    field_values = {
        'username': generators.StringGenerator(chars=
            string.ascii_letters + string.digits + '_'),
        'first_name': generators.LoremWordGenerator(1),
        'last_name': generators.LoremWordGenerator(1),
        'password': UNUSABLE_PASSWORD,
        # generate ten times more activated than deactivated users.
        'is_active': generators.ChoicesGenerator(values=[True] * 10 + [False]),
        # don't generate admin users
        'is_staff': False,
        'is_superuser': False,
        'date_joined': generators.DateTimeGenerator(max_date=datetime.now()),
        'last_login': generators.DateTimeGenerator(max_date=datetime.now()),
    }

    # don't follow permissions and groups
    follow_m2m = False

    def unique_email(self, model, instance):
        if User.objects.filter(email=instance.email):
            raise autofixture.InvalidConstraint(('email',))

    def prepare_class(self):
        self.add_constraint(self.unique_email)

    def post_process_instance(self, instance):
        if instance.last_login < instance.date_joined:
            instance.last_login = instance.date_joined
        return instance


autofixture.register(User, UserFixture, fail_silently=True)
