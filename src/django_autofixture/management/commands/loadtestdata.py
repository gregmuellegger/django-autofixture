# -*- coding: utf-8 -*-
from django.db.transaction import commit_on_success
from django.core.management.base import BaseCommand, CommandError
from django_autofixture import AutoFixture
from optparse import make_option


class Command(BaseCommand):
    help = 'Create random model instances for testing purposes.'
    args = 'app.Model:# [app.Model:# ...]'

    option_list = BaseCommand.option_list + (
        make_option('--no-follow-fk', action='store_true', dest='no_follow_fk',
            default=False, help='Nominates a specific database to load '
                'fixtures into. Defaults to the "default" database.'),
        make_option('--generate-fk', action='store_true', dest='generate_fk',
            default=False, help='Nominates a specific database to load '
                'fixtures into. Defaults to the "default" database.'),
        make_option('--no-follow-m2m', action='store_true', dest='no_follow_m2m',
            default=False, help='Nominates a specific database to load '
                'fixtures into. Defaults to the "default" database.'),
        make_option('--follow-m2m', action='store', dest='follow_m2m',
            default='1,5', help='Nominates a specific database to load '
                'fixtures into. Defaults to the "default" database.'),
        make_option('--generate-m2m', action='store', dest='generate_m2m',
            default='0,0', help='Nominates a specific database to load '
                'fixtures into. Defaults to the "default" database.'),
    )

    @commit_on_success
    def handle(self, *attrs, **options):
        from django.db.models import get_model

        follow_fk = not options['no_follow_fk']
        follow_m2m = not options['no_follow_m2m']
        if follow_m2m:
            follow_m2m = [int(i) for i in options['follow_m2m'].split(',')]
        generate_fk = options['generate_fk']
        generate_m2m = [int(i) for i in options['generate_m2m'].split(',')]

        verbosity = int(options['verbosity'])

        models = []
        for attr in attrs:
            app_label, model_label = attr.split('.')
            model_label, count = model_label.split(':')
            count = int(count)
            model = get_model(app_label, model_label)
            if not model:
                raise CommandError(
                    u'Unknown model: %s.%s' % (app_label, model_label))
            models.append((model, count))

        for model, count in models:
            fill = AutoFixture(
                model,
                follow_fk=follow_fk,
                generate_fk=generate_fk,
                follow_m2m=follow_m2m,
                generate_m2m=generate_m2m)
            for i, obj in enumerate(fill.iter(count)):
                if verbosity >= 1:
                    print('#%d %s(pk=%s): %s' % (
                        i+1,
                        '%s.%s' % (
                            model._meta.app_label,
                            model._meta.object_name),
                        unicode(obj.pk),
                        unicode(obj),
                    ))
