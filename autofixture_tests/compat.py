try:
    from unittest import skipIf
except ImportError:
    from django.utils.unittest import skipIf

try:
    from django.conf.urls.defaults import url
except ImportError:
    from django.conf.urls import url

try:
    from django.conf.urls.defaults import include
except ImportError:
    from django.conf.urls import include
