#!/usr/bin/env python
import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'autofixture_tests.settings'
parent = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, parent)

from django.test.simple import DjangoTestSuiteRunner


def runtests(*args):
    test_runner = DjangoTestSuiteRunner(interactive=False)
    failures = test_runner.run_tests(
        args or [
            'autofixture',
            'autofixture_tests',
            'autofixture_test',
            'generator_test',
            'values_tests',
            'sample_app',
        ],
        verbosity=1, interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
