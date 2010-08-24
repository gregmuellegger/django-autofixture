# -*- coding: utf-8 -*-


class InvalidConstraint(Exception):
    def __init__(self, fields, *args, **kwargs):
        self.fields = fields
        super(InvalidConstraint, self).__init__(*args, **kwargs)


def unique_constraint(model, instance):
    error_fields = []
    for field in instance._meta.fields:
        if field.unique:
            check = {field.name: getattr(instance, field.name)}
            unique = not bool(model._default_manager.filter(**check))
            if not unique:
                error_fields.append(field)
    if error_fields:
        raise InvalidConstraint(error_fields)


def unique_together_constraint(model, instance):
    error_fields = []
    if instance._meta.unique_together:
        for unique_fields in instance._meta.unique_together:
            check = {}
            for field_name in unique_fields:
                check[field_name] = getattr(instance, field_name)
            unique = not bool(model._default_manager.filter(**check))
            if not unique:
                error_fields.extend(
                    [instance._meta.get_field_by_name(field_name)[0]
                        for field_name in unique_fields])
    if error_fields:
        raise InvalidConstraint(error_fields)
