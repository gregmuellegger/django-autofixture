Changelog
=========

0.3.0
-----

* Adding better support for subclassing ``AutoFixture`` through merging of
  nested ``Values`` classes.
* Renamed attribute and argument ``none_chance`` to better matching name ``empty_p`` for generators
  and ``none_p`` for ``AutoFixture``.
* Fixed some issues with management command options. Thanks Mikko Hellsing for
  his hard work.
* Fixed issues in unregister(). Thanks Mikko Hellsing for the report.
* Adding support for ``FloatField``. Thanks to Jyr Gaxiola for the report.

0.2.5
-----

* Fixing issue with ``--generate-fk`` option in management command. Thanks
  Mikko Hellsing for the `report and fix`_.

.. _report and fix: http://github.com/gregmuellegger/django-autofixture/issues/issue/1/

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
