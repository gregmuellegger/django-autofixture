# -*- coding: utf-8 -*-
from django.db.models import fields


def unique_constraint(model, instance):
    for field in instance._meta.fields:
        if field.unique:
            check = {field.name: getattr(instance, field.name)}
            unique = not bool(model._default_manager.filter(**check))
            if not unique:
                return (field,)


def unique_together_constraint(model, instance):
    if instance._meta.unique_together:
        for fields in instance._meta.unique_together:
            check = {}
            for field_name in fields:
                check[field_name] = getattr(instance, field_name)
            unique = not bool(model._default_manager.filter(**check))
            if not unique:
                return [instance._meta.get_field_by_name(field_name)[0]
                    for field_name in fields]
