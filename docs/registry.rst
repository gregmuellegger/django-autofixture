The :class:`AutoFixture` registry
=================================

.. _registry:

Since :class:`AutoFixture` is designed to fit for almost all models, its very
generic and doesn't know anything about the actual logic and meanings of
relations or the purpose of your model fields. This makes it sometimes a bit
difficult to provide the correct :ref:`field_values <field values>` in all
places where you want ``autofixture`` to instanciate your models.

So there is a registry to register custom :class:`AutoFixture` subclasses with
specific models. These subclasses are then used by default if you generated
test data either with the :ref:`loadtestdata <loadtestdata>` management
command or with one of the :ref:`shortcuts <shortcuts>` in :mod:`autofixture`.

.. autofunction:: autofixture.register

.. autofunction:: autofixture.unregister

Default :class:`AutoFixture` subclasses
---------------------------------------

There are some :class:`AutoFixture` subclasses that are shipped by default
with ``django-autofixture``. These are listed below.

.. _UserFixture:
.. autoclass:: autofixture.autofixtures.UserFixture
   :members: __init__
