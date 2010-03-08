from autofixture.base import AutoFixture
from autofixture.constraints import InvalidConstraint


REGISTRY = {}


def register(model, autofixture, overwrite=False, fail_silently=False):
    from django.db import models
    if isinstance(model, basestring):
        model = models.get_model(*model.split('.', 1))
    if not overwrite and model in REGISTRY:
        if fail_silently:
            return
        raise ValueError(
            u'%s.%s is already registered. You can overwrite the registered '
            u'autofixture by providing the `overwrite` argument.' % (
                model._meta.app_label,
                model._meta.object_name,
            ))
    REGISTRY[model] = autofixture


def unregister(model_or_iterable, fail_silently=False):
    from django.db import models
    if isinstance(model_or_iterable, (list, tuple, set)):
        model_or_iterable = [model_or_iterable]
    for model in models:
        if isinstance(model, basestring):
            model = models.get_model(*model.split('.', 1))
        try:
            del REGISTRY[model]
        except KeyError:
            if fail_silently:
                continue
            raise ValueError(
                u'The model %s.%s is not registered.' % (
                    model._meta.app_label,
                    model._meta.object_name,
                ))





def create(model, count, *args, **kwargs):
    from django.db import models
    if isinstance(model, basestring):
        model = models.get_model(*model.split('.', 1))
    if model in REGISTRY:
        autofixture = REGISTRY[model](model, *args, **kwargs)
    else:
        autofixture = AutoFixture(model, *args, **kwargs)
    return autofixture.create(count)


def create_one(model, *args, **kwargs):
    return create(model, 1, *args, **kwargs)[0]


LOADING = False

def autodiscover():
    """
    Auto-discover INSTALLED_APPS autofixtures.py and tests.py modules and fail silently when
    not present. This forces an import on them to register any autofixture bits they
    may want.
    """
    from django.utils.importlib import import_module

    # Bail out if autodiscover didn't finish loading from a previous call so
    # that we avoid running autodiscover again when the URLconf is loaded by
    # the exception handler to resolve the handler500 view.  This prevents an
    # autofixtures.py module with errors from re-registering models and raising a
    # spurious AlreadyRegistered exception (see #8245).
    global LOADING
    if LOADING:
        return
    LOADING = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        # For each app, we need to look for an autofixture.py inside that app's
        # package. We can't use os.path here -- recall that modules may be
        # imported different ways (think zip files) -- so we need to get
        # the app's __path__ and look for autofixture.py on that path.

        # Step 1: find out the app's __path__ Import errors here will (and
        # should) bubble up, but a missing __path__ (which is legal, but weird)
        # fails silently -- apps that do weird things with __path__ might
        # need to roll their own autofixture registration.
        mod = import_module(app)
        try:
            app_path = mod.__path__
        except AttributeError:
            continue

        # Step 2: use imp.find_module to find the app's autofixtures.py. For some
        # reason imp.find_module raises ImportError if the app can't be found
        # but doesn't actually try to import the module. So skip this app if
        # its autofixtures.py doesn't exist
        try:
            imp.find_module('autofixtures', app_path)
        except ImportError:
            continue

        # Step 3: import the app's autofixtures file. If this has errors we want them
        # to bubble up.
        import_module("%s.autofixtures" % app)

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            app_path = mod.__path__
        except AttributeError:
            continue

        try:
            imp.find_module('tests', app_path)
        except ImportError:
            continue

        import_module("%s.tests" % app)

    # autodiscover was successful, reset loading flag.
    LOADING = False
