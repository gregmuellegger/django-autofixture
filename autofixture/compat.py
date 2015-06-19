import django


try:
    from django.contrib.contenttypes.fields import GenericForeignKey
# For Django 1.6 and earlier
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey


try:
    from django.contrib.contenttypes.fields import GenericRelation
# For Django 1.6 and earlier
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation


try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict


try:
    import importlib
except ImportError:
    from django.utils import importlib


try:
    from django.db.transaction import atomic
# For django 1.5 and earlier
except ImportError:
    from django.db.transaction import commit_on_success as atomic


try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models import get_model


def get_field(model, field_name):
    if django.VERSION < (1, 8):
        return model._meta.get_field_by_name(field_name)[0]
    else:
        return model._meta.get_field(field_name)
