# -*- coding: utf-8 -*-
from django.db import models
from django.db.transaction import commit_on_success
from django.core.management.base import BaseCommand, CommandError
from django_autofixture import signals, AutoFixture
from optparse import make_option


class Command(BaseCommand):
    help = 'Create random model instances for testing purposes.'
    args = 'app.Model:# [app.Model:# ...]'

    # TODO(gregor@muellegger.de): change descriptions, they are already
    # invalid

    option_list = BaseCommand.option_list + (
        make_option('-d', '--overwrite-defaults', action='store_true',
            dest='overwrite_defaults', default=False, help=
                u'Generate values for fields with default values. Default is '
                u'to use default values.'),
        make_option('--no-follow-fk', action='store_true', dest='no_follow_fk',
            default=False, help=
                u'Ignore ForeignKey fields while creating model instances.'),
        make_option('--generate-fk', action='store', dest='generate_fk',
            default='', help=
                u'Do not use already existing instances for ForeignKey '
                u'relations. Create new instances instead.'),
        make_option('--no-follow-m2m', action='store_true',
            dest='no_follow_m2m', default=False, help=
                u'Ignore ManyToManyFields while creating model instances.'),
        make_option('--follow-m2m', action='store', dest='follow_m2m',
            default='1:5', help=
                u'Specify minimum and maximum number of instances that are '
                u'assigned to a m2m relation. Use two, comma separated '
                u'numbers in the form of: min,max. Default is 1,5.'),
        make_option('--generate-m2m', action='store', dest='generate_m2m',
            default='', help=
                u'Specify minimum and maximum number of instances that are '
                u'newly created and assigned to a m2m relation. Use two, '
                u'comma separated numbers in the form of: min,max. Default is '
                u'0,0 which means that no related models are created.'),
    )

    def format_output(self, obj):
        output = unicode(obj)
        if len(output) > 50:
            output = u'%s ...' % output[:50]
        return output

    def print_instance(self, sender, model, instance, **kwargs):
        if self.verbosity < 1:
            return
        print '%s(pk=%s): %s' % (
            '%s.%s' % (
                model._meta.app_label,
                model._meta.object_name),
            unicode(instance.pk),
            self.format_output(instance),
        )
        if self.verbosity < 2:
            return
        for field in instance._meta.fields:
            if isinstance(field, models.ForeignKey):
                obj = getattr(instance, field.name)
                if isinstance(obj, models.Model):
                    print '|   %s (pk=%s): %s' % (
                        field.name,
                        obj.pk,
                        self.format_output(obj))
        for field in instance._meta.many_to_many:
            qs = getattr(instance, field.name).all()
            if qs.count():
                print '|   %s (count=%d):' % (
                    field.name,
                    qs.count())
                for obj in qs:
                    print '|   |   (pk=%s): %s' % (
                        obj.pk,
                        self.format_output(obj))

    @commit_on_success
    def handle(self, *attrs, **options):
        from django.db.models import get_model

        follow_fk = not options['no_follow_fk']
        follow_m2m = not options['no_follow_m2m']
        generate_fk = options['generate_fk'].split(',')

        error_option = None
        try:
            if follow_m2m:
                value = [i for i in options['follow_m2m'].split(',')]
                if len(value) == 1 and value[0].count(':') == 1:
                    follow_m2m = [int(i) for i in value[0].split(':')]
                else:
                    follow_m2m = {}
                    for field in value:
                        key, minval, maxval = field.split(':')
                        follow_m2m[key] = int(minval), int(maxval)
        except ValueError:
            error_option = '--follow-m2m=%s' % options['follow_m2m']
        try:
            value = [v for v in options['generate_m2m'].split(',') if v]
            if len(value) == 1 and value[0].count(':') == 1:
                generate_m2m = [int(i) for i in value[0].split(':')]
            else:
                generate_m2m = {}
                for field in value:
                    key, minval, maxval = field.split(':')
                    generate_m2m[key] = int(minval), int(maxval)
        except ValueError:
            error_option = '--generate-m2m=%s' % options['generate_m2m']
        if error_option:
            raise CommandError(
                u'Invalid option %s\n'
                u'Expected: %s=field:min:max,field2:min:max... (min and max must be numbers)' % (
                    error_option,
                    error_option.split('=', 1)[0]))

        overwrite_defaults = options['overwrite_defaults']

        self.verbosity = int(options['verbosity'])

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

        signals.instance_created.connect(
            self.print_instance)

        for model, count in models:
            fill = AutoFixture(
                model,
                overwrite_defaults=overwrite_defaults,
                follow_fk=follow_fk,
                generate_fk=generate_fk,
                follow_m2m=follow_m2m,
                generate_m2m=generate_m2m)
            for obj in fill.iter(count):
                pass
