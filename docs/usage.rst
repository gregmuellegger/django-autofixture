.. _usage:

Howto use the library
=====================

Its easy to get started with the :doc:`loadtestdata management command
<loadtestdata>` but its quite limited if you want to have more control of how
your test data should be created. This chapter describes how you use the
library in your python environment like the shell, a custom script or in
unittests.

Creating model instances
------------------------

The :mod:`autofixture` module contains a few shortcuts to make the creation of
test data as fast as possible.

.. _shortcuts:

.. autofunction:: autofixture.create

.. autofunction:: autofixture.create_one

.. _AutoFixture:

Using the :class:`~autofixture.base.AutoFixture` class
------------------------------------------------------

.. autoclass:: autofixture.base.AutoFixture
   :members: __init__, add_field_value, add_constraint,
       create, create_one

The :class:`~autofixture.base.AutoFixture` registry
---------------------------------------------------

.. _registry:

Since :class:`~autofixture.base.AutoFixture` is designed to fit for almost all
models, its very generic and doesn't know anything about the actual logic and
meanings of relations or the purpose of your model fields. This makes it
sometimes a bit difficult to provide the correct ``field_values`` in all
places where you want ``autofixture`` to instanciate your models.

So there is a registry to register custom
:class:`~autofixture.base.AutoFixture` subclasses with specific models. These
subclasses are then used by default if you generate test data either with the
:ref:`loadtestdata <loadtestdata>` management command or with one of the
:ref:`shortcuts <shortcuts>` in :mod:`autofixture`.

.. autofunction:: autofixture.register

.. autofunction:: autofixture.unregister

.. autofunction:: autofixture.get

Subclassing :class:`AutoFixture`
--------------------------------

.. _subclassing:
.. _values:

In most cases it will by sufficient to provide a different logic to generate
the values for your model fields in :class:`~autofixture.base.AutoFixture`
subclasses. This can be simply done by a nested ``Values`` class::

    class EntryFixture(AutoFixture):
        class Values:
            title = 'My static title'
            status = staticmethod(lambda: random.choice((1,2)))
            pub_date = generators.DateTimeGenerator(
                min_date=datetime(2009,1,1),
                max_date=datetime(2009,12,31))

This will make sure that ``title`` is always ``'My static title'``, status is
either ``1`` or ``2`` and that ``pub_date`` is in the somewhere in 2009.

Like you can see in the example you can apply static values, simple callables
or specific generators to specific fields. However remember to use the
``staticmethod`` decorator when using a ``method`` as callable - like the
``lambda`` statement in the example. It's in fact also just a shorter
definition of a method.

*A note on subclassing subclasses and turtles all the way down:* Sometimes
it's usefull for a project to have a common base class for all the registered
*AutoFixtures*. This is possible and easy since you don't need
to re-define all the field definitions in the nested ``Values`` class. The
:class:`~autofixture.base.AutoFixture` class cares about this and will
collect all ``Values`` of base classes and merge them together. For
clarification here a short example::

    class CommonFixture(AutoFixture):
        class Values:
            tags = generators.ChoicesGenerator(
                values=('apple', 'banana', 'orange'))

    class EntryFixture(AutoFixture):
        class Values:
            title = 'My static title'

    # all created entries will have the same title 'My static title' and one
    # tag out of apple, banana and orange.
    EntryFixture(Entry).create(5)

If you want to digg deeper and need to customize more logic of model creation,
you can override some handy methods of the
:class:`~autofixture.base.AutoFixture` class:

.. automethod:: autofixture.base.AutoFixture.prepare_class

.. automethod:: autofixture.base.AutoFixture.post_process_instance

.. automethod:: autofixture.base.AutoFixture.get_generator
