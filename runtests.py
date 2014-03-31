#!/usr/bin/env python
import os, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'autofixture_tests.settings'
parent = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, parent)


def runtests(*args):
    from django.core.management import execute_from_command_line
    args = args or [
        'autofixture',
        'autofixture_tests',
    ]
    execute_from_command_line([sys.argv[0], 'test'] + args)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
