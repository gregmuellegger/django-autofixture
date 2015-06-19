Changelog
=========

0.10.1
------

* Fixing unique constraint checks for multiple ``None`` values. Thanks to
  Andrew Lewisohn for the patch. See `#66`_.

.. _#66: https://github.com/gregmuellegger/django-autofixture/pull/66

0.10.0
------

* Supporting Django 1.7 style app configs in ``settings.INSTALLED_APPS``
  when auto-importing autofixture definitions with
  ``autofixture.autodiscover``.
* Adding ``autofixture.generators.PositiveDecimalGenerator``.

0.9.2
-----

* Fixed ``UserFixture`` that generated usernames with more than 30 characters.

0.9.1
-----

* Fixed unique constraint for models that have multiple unique_togethers set.

0.9
---
* Make ``ImageGenerator`` consider the given file storage. Thanks to Andrew
  Pashkin for the patch.
* Fixing check for unique constraint during data generation if the field
  allows to be nullable. Thanks for Andrew Pashkin for the report and fix.

0.8.0
-----

* Adding support for django's ``ImageField``. Thanks to Visgean Skeloru for
  the patch.

0.7.0
-----

* Adding ``AutoFixture.pre_process_instance`` method.
* Allow arbitrary keyword arguments for ``AutoFixture.create`` method.
* Fixing ``autofixture.unregister`` function.
* Fixing ``UserFixture.post_process_instance``.

0.6.3
-----

* Fixing long stated issue with GenericRelation fields. Thanks to StillNewb
  for the patch.

0.6.2
-----

* Supporting Django 1.6.

0.6.1
-----

* Fixing issue with models that have a selfreferencing ForeignKey field.
  Thanks to Josh Fyne for the patch.

0.6.0
-----

* Adding ``generators.WeightedGenerator`` for propabilistic selection of
  values. Thanks to Jonathan Tien for the idea and patch.
* Supporting model inheritance. Thanks to Josh Fyne for the patch.

0.5.0
-----

* Adding ``FirstNameGenerator`` and ``LastNameGenerator``. Thanks to Jonathan
  Tien for the initial patch.
* Registered Autofixtures are used for models that are created for foreignkeys
  and many to many relations. Thanks to Theo Spears for the report.

0.4.0
-----

* Python 3 support! Though we had to drop Python 2.5 support. If you cannot
  upgrade to Python 2.6 by yet, please consider using the 0.3.x versions of
  django-autofixture.
  By the way: by Python 3 support, I mean, that the test suite is running
  without any errors. I have not tested yet the library in production for
  Python 3. So please test and submit bug reports if you encounter any.

0.3.2
-----

* ``DateTimeField`` receive timezone aware datetime objects now. Thanks to
  Scott Woodall for the report and patch.
* Adding ``static_domain`` parameter to ``EmailGenerator`` to allow the
  production of emails that will always have the same domain. Thanks to
  mvdwaeter for the initial patch.

0.3.1
-----

* ``field_values`` were not picked up if there was a default value assigned to
  the field. Thanks to sirex for the report.

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
