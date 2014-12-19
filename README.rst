==================
django-autofixture
==================

.. image:: https://travis-ci.org/gregmuellegger/django-autofixture.png
   :alt: Build Status
   :target: https://travis-ci.org/gregmuellegger/django-autofixture

This app aims to provide a simple way of loading masses of randomly generated
test data into your development database. You can use a management command to
load test data through command line.

It is named *autofixture* because of the similarity of how I mainly used
django's fixtures. Usually you add test data through the admin to see how your
site looks with non static pages. You export data by using ``dumpdata`` to
send it to your colleagues or to preserve it before you make a ``manage.py
reset app`` and so on. Your site gets more and more complex and adding test
data gets more and more annoying.

This is the usecase where autofixtures should help you to save time that can
actually be spent on hacking.


Installation
============

You must make the ``autofixture`` package available on your python path.
Either drop it into your project directory or install it from the python
package index with ``pip install django-autofixture``. You can also use
``easy_install django-autofixture`` if you don't have pip available.

To use the management command you must add ``'autofixture'`` to the
``INSTALLED_APPS`` setting in your django settings file. You don't need to do
this if you want to use the ``autofixture`` package only as library.


Management command
==================

The ``loadtestdata`` accepts the following syntax::

    python manage.py loadtestdata [options] app.Model:# [app.Model:# ...]

Its nearly self explanatory. Supply names of models, prefixed with its app
name. After that, place a colon and tell the command how many objects you want
to create. Here is an example how to create three categories and twenty
entries for you blogging app::

    python manage.py loadtestdata blog.Category:3 blog.Entry:20

Voila! You have ready to use testing data populated to your database. The
model fields are filled with data by producing randomly generated values
depending on the type of the field. E.g. text fields are filled with lorem
ipsum dummies, date fields are populated with random dates from the last
years etc.

There are a few command line options available. Mainly to control the
behavior of related fields. If foreingkey or many to many fields should be
populated with existing data or if the related models are also generated on
the fly. Please have a look at the help page of the command for more
information::

    python manage.py help loadtestdata


Using autofixtures as tool for unittests
========================================

It has proofed that autofixtures have a great use for unittests. It has always
bugged me that creating complex models for testing their behaviour was
complicated. Sometimes models have strict restrictions or many related objects
which they depend on. One solution would be to use traditional fixtures
dumped from your production database. But while in development when database
schemes are changing frequently, its hard to maintain all fixtures and to know
exactly which objects are contained in the dumps etc...

Autofixtures to the rescue! It lets you automatically generate models and all
of their dependecies on the fly. Have a look at the following examples.

Lets start with the very basics. We create an ``AutoFixture`` instance for the
``Entry`` model and tell it to create ten model instances::

    from autofixture import AutoFixture
    fixture = AutoFixture(Entry)
    entries = fixture.create(10)

Now you can play around and test your blog entries. By default dependecies of
foreignkeys and many to many relations are solved by randomly selecting an
already existing object of the related model. What if you don't have one yet?
You can provide the ``generate_fk`` attribute which allows the autofixture
instance to follow foreignkeys by generating new related models::

    fixture = AutoFixture(Entry, generate_fk=True)

This generates new instance for *all* foreignkey fields of ``Entry``. Unless
the model has a foreign key reference to itself, wherein the field will be set
to None if allowed or raise a ``CreateInstanceError`` if not. This is to prevent
max recursion depth errors. Its possible to limit this behaviour to single fields::

    fixture = AutoFixture(Entry, generate_fk=['author'])

This will only create new authors automatically and doesn't touch other
tables. The same is possible with many to many fields. But you need
additionally specify how many objects should be created for the m2m relation::

    fixture = AutoFixture(Entry, generate_m2m={'categories': (1,3)})

All created entry models get one to three new categories assigned.

Setting custom values for fields
--------------------------------

However its often necessary to be sure that a specific field must have a
specific value. This is easily achieved with the ``field_values`` attribute of
``AutoFixture``::

    fixture = AutoFixture(Entry,
        field_values={'pub_date': datetime(2010, 2, 1)})


Limiting the set of models assigned to a ForeignKey field
----------------------------------------------------------

You could, for example, limit the Users assigned to a foreignkey field to only 
non-staff Users.  Or create Entries for all Blogs not belonging to Yoko Ono.  
Use the same construction as ForeignKey.limit_choices_to_ attribute::

    from autofixture import AutoFixture, generators
    fixture = AutoFixture(Entry,
            field_values={
                'blog': generators.InstanceSelector(Blog, 
                    limit_choices_to={'name__ne':"Yoko Ono's blog"})
                          } )

    

Custom autofixtures
===================

To have custom autofixtures for your model, you can easily subclass
``AutoFixture`` somewhere (e.g. in myapp/autofixtures.py) ::

    from models import MyModel
    from autofixture import generators, register, AutoFixture

    class MyModelAutoFixture(AutoFixture):
        field_values = {
            'name': generators.StaticGenerator('this_is_my_static_name'),
        }

    register(MyModel, MyModelAutoFixture)


Then, ``loadtestdata`` will automatically use your custom fixtures. ::

    python manage.py loadtestdata app.MyModel:10

You can load all ``autofixtures.py`` files of your installed apps
automatically like you can do with the admin autodiscover. Do so by running
``autofixture.autodiscover()`` somewhere in the code, preferably in the
``urls.py``.


More
====

There is so much more to explore which might be useful for you and your
projects:

* There are ways to register custom ``AutoFixture`` subclasses with models
  that are automatically used when calling ``loadtestdata`` on the model.
* More control for related models, even with relations of related models...
  (e.g. by using ``generate_fk=['author', 'author__user']``)
* Custom constraints that are used to ensure that created the models are
  valid (e.g. ``unique`` and ``unique_together`` constraints which are
  already handled by default)

I hope to explain this in the future with more details in a documentation. It
will be written but is not finished yet. I wanted to get this project out to
support you in development. But since its only python code you can easily
study the source on your own and see in which ways it can be used. There are
already some parts documented with doc strings which might also be helpful for you.


Contribute
==========

You can find the latest development version on github_. Get there and fork it,
file bugs or send me nice wishes.

To start developing, make sure the test suite passes::
    
    virtualenv .env
    source .env/bin/activate
    pip install -r requirements/tests.txt
    python setup.py test

Now go, do some coding.

Feel free to drop me a message about critique or feature requests. You can get
in touch with me by mail_ or twitter_.

Happy autofixturing!

.. _github: https://github.com/gregmuellegger/django-autofixture
.. _mail: mailto:gregor@muellegger.de
.. _twitter: http://twitter.com/gregmuellegger
.. _ForeignKey.limit_choices_to: http://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.limit_choices_to
