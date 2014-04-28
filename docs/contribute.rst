Contribute
==========

If you want to use an isolated environment while hacking on
``django-autofixture`` you can run the following commands from the project's
root directory::

    virtualenv . --no-site-packages
    source bin/activate
    pip install -r requirements/tests.txt

Please run now the tests that are shipped with ``autofixture`` to see if
everything is working::

    python runtests.py

Happy hacking!
