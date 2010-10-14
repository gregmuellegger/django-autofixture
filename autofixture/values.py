from UserDict import UserDict, IterableUserDict


class ValuesMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        parent_value_attrs = {}
        # left most base class overwrites righter base classes
        for base in bases[::-1]:
            if hasattr(base, '_value_attrs'):
                parent_value_attrs.update(base._value_attrs)
        defined_value_attrs = {}
        for key in attrs:
            if not key.startswith('__'):
                defined_value_attrs[key] = attrs[key]

        for key in defined_value_attrs:
            del attrs[key]

        attrs['_value_attrs'] = {}
        attrs['_value_attrs'].update(parent_value_attrs)
        attrs['_value_attrs'].update(defined_value_attrs)
        return super(ValuesMetaclass, mcs).__new__(mcs, name, bases, attrs)


class ValuesBase(IterableUserDict, object):
    def __init__(self, *parents, **values):
        self.data = self._value_attrs.copy()
        for parent in parents:
            if parent is None:
                continue
            if isinstance(parent, (dict, UserDict)):
                self.data.update(parent)
            else:
                for attr in dir(parent):
                    if not attr.startswith('__'):
                        self.data[attr] = getattr(parent, attr)
        self.data.update(**values)

    def __add__(self, other):
        return self.__class__(self, other)

    def __radd__(self, other):
        return self.__class__(other, self)

    def __iadd__(self, other):
        self.data.update(other)
        return self


class Values(ValuesBase):
    __metaclass__ = ValuesMetaclass
