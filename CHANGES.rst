Changelog
=========

0.2.4
-----

* Using ``Autofixture.Values`` for defining initial values in ``Autofixture``
  subclasses.

* Making autodiscover more robust. Don't break if some module can't be
  imported or throws any other exception.

0.2.3
-----

* Fixing bug when a ``CharField`` with ``max_length`` smaller than 15 is used.

* ``AutoFixture.field_values`` accepts callables as values.
