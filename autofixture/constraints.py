# -*- coding: utf-8 -*-


class InvalidConstraint(Exception):
    def __init__(self, fields, *args, **kwargs):
        self.fields = fields
        super(InvalidConstraint, self).__init__(*args, **kwargs)


def unique_constraint(model, instance):
    error_fields = []
    for field in instance._meta.fields:
        if (
                field.unique and
                not field.primary_key and
                getattr(instance, field.name) is not None):
            check = {field.name: getattr(instance, field.name)}

            unique = model._default_manager.filter(**check).count() == 0
            if not unique:
                error_fields.append(field)
    if error_fields:
        raise InvalidConstraint(error_fields)


def unique_together_constraint(model, instance):
    if not instance._meta.unique_together:
        return
    error_fields = []
    for unique_fields in instance._meta.unique_together:
        check = {}
        for field_name in unique_fields:
            if not instance._meta.get_field_by_name(field_name)[0].primary_key:
                check[field_name] = getattr(instance, field_name)
        if all(e is None for e in check.values()):
            continue
        unique = model._default_manager.filter(**check).count() == 0
        if not unique:
            error_fields.extend(
                [instance._meta.get_field_by_name(field_name)[0]
                    for field_name in unique_fields])
    if error_fields:
        raise InvalidConstraint(error_fields)
