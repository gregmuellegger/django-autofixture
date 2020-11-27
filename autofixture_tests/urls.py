# -*- coding: utf-8 -*-
from django.http import HttpResponse


def handle404(request, exception=None):
    return HttpResponse('404')


def handle500(request, exception=None):
    return HttpResponse('500')

handler404 = 'autofixture_tests.urls.handle404'
handler500 = 'autofixture_tests.urls.handle500'


urlpatterns = [
]
