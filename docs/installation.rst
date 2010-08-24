Installation
============

Download and install with ``pip`` or ``easy_install``
-----------------------------------------------------

You can install the ``django-autofixture`` like any other python package. The
prefered way is to use `pip <http://pypi.python.org/pypi/pip>`_. Please run the
following command in your terminal::

    pip install django-autofixture

This will install the package in your system wide python installation.

You can fall back to the :command:`easy_install` command if :command:`pip` is
not available on your system::

    easy_install django-autofixture

.. note:: In most cases you need admin previlegies to install a package into
   your system. You can get these previlegies by prefixing the commands above
   with ``sudo``.

.. _INSTALLED_APPS:

Add ``autofixture`` to your django project
------------------------------------------

Usually you want to add ``autofixture`` to your ``INSTALLED_APPS`` in the
settings file of your django project. This will make the :ref:`loadtestdata
<loadtestdata>` management command available to your use.

Using the development version
-----------------------------

You can ofcourse also install and use the current development version. All you
need is to have the `git <http://git-scm.com/>`_ and `setuptools
<http://pypi.python.org/pypi/setuptools>`_ installed.

Now get the repository from `github
<http://github.net/gregmuellegger/django-autofixture>`_ and run::

    git clone git://github.com/gregmuellegger/django-autofixture.git

This will download the project into your local directory. :command:`cd` to the
``django-autofixture`` directory and run::

    python setup.py install

Now follow the instructions under :ref:`INSTALLED_APPS` and everything will be
in place to use ``django-autofixture``.
