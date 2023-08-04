import json

from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.forms import JSONField as JSONFormField


class SRPatchedJSONFormField(JSONFormField):
    """
    Overrides `prepare_value` to return value as it is without dumping to json, and thus
      re-encoding over and over again
    """

    def prepare_value(self, value):
        """
        Exclude returning None in case of {}, returning None makes the field empty when loaded
        from admin instead of returning {},
        which causes an error where empty dict was expected
        """
        if not value == {} and value in self.empty_values:
            return None
        elif isinstance(value, str):
            return value
        else:
            return super(SRPatchedJSONFormField, self).prepare_value(value)


class SRPatchedJSONField(JSONField):
    """
    Overrides
    1. `formfield` to set our custom JSON field as `form_class`
    2. `from_db_value` to return a json from `str`
    """

    def formfield(self, **kwargs):
        defaults = {"form_class": SRPatchedJSONFormField}
        defaults.update(kwargs)
        return super(JSONField, self).formfield(**defaults)

    def from_db_value(self, value, expression, connection, context):
        """
        To solve https://bitbucket.org/schinckel/django-jsonfield/issues/57/cannot-use-in-the-same-project-as-djangos
        """
        if isinstance(value, str):
            try:
                return json.loads(value)
            except ValueError:
                return value

        return value
