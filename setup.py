#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name = '',
    version = '1.0',
    url = 'http://github.com/jacobian/django-shorturls',
    license = 'BSD',
    description = '',
    author = u'Gregor Müllegger',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
