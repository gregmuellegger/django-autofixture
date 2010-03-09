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

Using the :class:`AutoFixture` class
------------------------------------

.. autoclass:: autofixture.base.AutoFixture
   :members: __init__, add_field_value, add_constraint, check_constrains,
       create, create_one

Subclassing :class:`AutoFixture`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following methods may be overwritten by subclasses:

.. automethod:: autofixture.base.AutoFixture.prepare_class

.. automethod:: autofixture.base.AutoFixture.post_process_instance

.. automethod:: autofixture.base.AutoFixture.get_generator
