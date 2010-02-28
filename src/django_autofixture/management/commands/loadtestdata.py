# -*- coding: utf-8 -*-
from django.db.transaction import commit_on_success
from django.core.management.base import BaseCommand, CommandError
from django_autofixture import AutoFixture
from optparse import make_option


class Command(BaseCommand):
    help = 'Create random model instances for testing purposes.'
    args = 'app.Model:# [app.Model:# ...]'

    option_list = BaseCommand.option_list + (
        make_option('-d', '--overwrite-defaults', action='store_true',
            dest='overwrite_defaults', default=False, help=
                u'Generate values for fields with default values. Default is '
                u'to use default values.'),
        make_option('--no-follow-fk', action='store_true', dest='no_follow_fk',
            default=False, help=
                u'Ignore ForeignKey fields while creating model instances.'),
        make_option('--generate-fk', action='store_true', dest='generate_fk',
            default=False, help=
                u'Do not use already existing instances for ForeignKey '
                u'relations. Create new instances instead.'),
        make_option('--no-follow-m2m', action='store_true',
            dest='no_follow_m2m', default=False, help=
                u'Ignore ManyToManyFields while creating model instances.'),
        make_option('--follow-m2m', action='store', dest='follow_m2m',
            default='1,5', help=
                u'Specify minimum and maximum number of instances that are '
                u'assigned to a m2m relation. Use two, comma separated '
                u'numbers in the form of: min,max. Default is 1,5.'),
        make_option('--generate-m2m', action='store', dest='generate_m2m',
            default='0,0', help=
                u'Specify minimum and maximum number of instances that are '
                u'newly created and assigned to a m2m relation. Use two, '
                u'comma separated numbers in the form of: min,max. Default is '
                u'0,0 which means that no related models are created.'),
    )

    @commit_on_success
    def handle(self, *attrs, **options):
        from django.db.models import get_model

        follow_fk = not options['no_follow_fk']
        follow_m2m = not options['no_follow_m2m']
        generate_fk = options['generate_fk']

        error_option = None
        try:
            if follow_m2m:
                follow_m2m = [int(i) for i in options['follow_m2m'].split(',')]
        except ValueError:
            error_option = '--follow-m2m=%s' % options['follow_m2m']
        try:
            generate_m2m = [int(i) for i in options['generate_m2m'].split(',')]
        except ValueError:
            error_option = '--generate-m2m=%s' % options['generate_m2m']
        if error_option:
            raise CommandError(
                u'Invalid option %s\n'
                u'Expected: %s=min,max (min and max must be numbers)' % (
                    error_option,
                    error_option.split('=', 1)[0]))

        overwrite_defaults = options['overwrite_defaults']

        verbosity = int(options['verbosity'])

        models = []
        for attr in attrs:
            try:
                app_label, model_label = attr.split('.')
                model_label, count = model_label.split(':')
                count = int(count)
            except ValueError:
                raise CommandError(
                    u'Invalid argument: %s\n'
                    u'Expected: app_label.ModelName:count '
                    u'(count must be a number)' % (
                        attr,
                    )
                )
            model = get_model(app_label, model_label)
            if not model:
                raise CommandError(
                    u'Unknown model: %s.%s' % (app_label, model_label))
            models.append((model, count))

        for model, count in models:
            fill = AutoFixture(
                model,
                overwrite_defaults=overwrite_defaults,
                follow_fk=follow_fk,
                generate_fk=generate_fk,
                follow_m2m=follow_m2m,
                generate_m2m=generate_m2m)
            for i, obj in enumerate(fill.iter(count)):
                if verbosity >= 1:
                    reprstr = unicode(obj)
                    if len(reprstr) > 50:
                        reprstr = u'%s ...' % reprstr[:50]
                    print('#%d %s(pk=%s): %s' % (
                        i+1,
                        '%s.%s' % (
                            model._meta.app_label,
                            model._meta.object_name),
                        unicode(obj.pk),
                        reprstr,
                    ))
