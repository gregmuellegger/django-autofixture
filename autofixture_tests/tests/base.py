# -*- coding: utf-8 -*-
import sys
import autofixture
from decimal import Decimal
from datetime import date, datetime
from django.test import TestCase
from autofixture import generators
from autofixture.base import AutoFixture, CreateInstanceError,  Link
from autofixture.values import Values
from ..models import y2k
from ..models import (
    SimpleModel, OtherSimpleModel, DeepLinkModel1, DeepLinkModel2,
    NullableFKModel, BasicModel, UniqueTestModel, UniqueTogetherTestModel,
    RelatedModel, O2OModel, InheritModel, InheritUniqueTogetherModel,
    M2MModel, ThroughModel, M2MModelThrough, SelfReferencingModel,
    SelfReferencingModelNoNull, GFKModel, GRModel)


if sys.version_info[0] < 3:
    str_ = unicode
else:
    str_ = str


class SimpleAutoFixture(AutoFixture):
    field_values = {
        'name': generators.StaticGenerator('foo'),
    }


class BasicValueFixtureBase(AutoFixture):
    field_values = Values(blankchars='bar')


class BasicValueFixture(BasicValueFixtureBase):
    class Values:
        chars = 'foo'
        shortchars = staticmethod(lambda: 'a')
        intfield = generators.IntegerGenerator(min_value=1, max_value=13)

    field_values = {
        'nullchars': 'spam',
    }


class TestBasicModel(TestCase):
    def assertEqualOr(self, first, second, fallback):
        if first != second and not fallback:
            self.fail()

    def test_create(self):
        filler = AutoFixture(BasicModel)
        filler.create(10)
        self.assertEqual(BasicModel.objects.count(), 10)

    def test_constraints(self):
        filler = AutoFixture(
            BasicModel,
            overwrite_defaults=False)
        for obj in filler.create(100):
            self.assertTrue(len(obj.chars) > 0)
            self.assertEqual(type(obj.chars), str_)
            self.assertTrue(len(obj.shortchars) <= 2)
            self.assertEqual(type(obj.shortchars), str_)
            self.assertTrue(type(obj.blankchars), str_)
            self.assertEqualOr(type(obj.nullchars), str_, None)
            self.assertEqual(type(obj.slugfield), str_)
            self.assertEqual(type(obj.defaultint), int)
            self.assertEqual(obj.defaultint, 1)
            self.assertEqual(type(obj.intfield), int)
            self.assertEqual(type(obj.sintfield), int)
            self.assertEqual(type(obj.pintfield), int)
            self.assertEqual(type(obj.psintfield), int)
            self.assertEqual(type(obj.datefield), date)
            self.assertEqual(type(obj.datetimefield), datetime)
            self.assertEqual(type(obj.defaultdatetime), datetime)
            self.assertEqual(obj.defaultdatetime, y2k())
            self.assertEqual(type(obj.decimalfield), Decimal)
            self.assertTrue('@' in obj.emailfield)
            self.assertTrue('.' in obj.emailfield)
            self.assertTrue(' ' not in obj.emailfield)
            self.assertTrue(obj.ipaddressfield.count('.'), 3)
            self.assertTrue(len(obj.ipaddressfield) >= 7)
        self.assertEqual(BasicModel.objects.count(), 100)

    def test_field_values(self):
        int_value = 1
        char_values = (u'a', u'b')
        filler = AutoFixture(
            BasicModel,
            field_values={
                'intfield': 1,
                'chars': generators.ChoicesGenerator(values=char_values),
                'shortchars': lambda: u'ab',
            })
        for obj in filler.create(100):
            self.assertEqual(obj.intfield, int_value)
            self.assertTrue(obj.chars in char_values)
            self.assertEqual(obj.shortchars, u'ab')

    def test_field_values_overwrite_defaults(self):
        fixture = AutoFixture(
            BasicModel,
            field_values={
                'defaultint': 42,
            })
        obj = fixture.create(1)[0]
        self.assertEqual(obj.defaultint, 42)


class TestRelations(TestCase):
    def test_generate_foreignkeys(self):
        filler = AutoFixture(
            RelatedModel,
            generate_fk=True)
        for obj in filler.create(100):
            self.assertEqual(obj.related.__class__, BasicModel)
            self.assertEqual(obj.limitedfk.name, 'foo')

    def test_deep_generate_foreignkeys(self):
        filler = AutoFixture(
            DeepLinkModel2,
            generate_fk=True)
        for obj in filler.create(10):
            self.assertEqual(obj.related.__class__, DeepLinkModel1)
            self.assertEqual(obj.related.related.__class__, SimpleModel)
            self.assertEqual(obj.related.related2.__class__, SimpleModel)

    def test_deep_generate_foreignkeys2(self):
        filler = AutoFixture(
            DeepLinkModel2,
            follow_fk=False,
            generate_fk=('related', 'related__related'))
        for obj in filler.create(10):
            self.assertEqual(obj.related.__class__, DeepLinkModel1)
            self.assertEqual(obj.related.related.__class__, SimpleModel)
            self.assertEqual(obj.related.related2, None)

    def test_generate_only_some_foreignkeys(self):
        filler = AutoFixture(
            RelatedModel,
            generate_fk=('related',))
        for obj in filler.create(100):
            self.assertEqual(obj.related.__class__, BasicModel)
            self.assertEqual(obj.limitedfk, None)

    def test_follow_foreignkeys(self):
        related = AutoFixture(BasicModel).create()[0]
        self.assertEqual(BasicModel.objects.count(), 1)

        simple = SimpleModel.objects.create(name='foo')
        simple2 = SimpleModel.objects.create(name='bar')

        filler = AutoFixture(
            RelatedModel,
            follow_fk=True)
        for obj in filler.create(100):
            self.assertEqual(obj.related, related)
            self.assertEqual(obj.limitedfk, simple)

    def test_follow_only_some_foreignkeys(self):
        related = AutoFixture(BasicModel).create()[0]
        self.assertEqual(BasicModel.objects.count(), 1)

        simple = SimpleModel.objects.create(name='foo')
        simple2 = SimpleModel.objects.create(name='bar')

        filler = AutoFixture(
            RelatedModel,
            follow_fk=('related',))
        for obj in filler.create(100):
            self.assertEqual(obj.related, related)
            self.assertEqual(obj.limitedfk, None)

    def test_follow_fk_for_o2o(self):
        # OneToOneField is the same as a ForeignKey with unique=True
        filler = AutoFixture(O2OModel, follow_fk=True)

        simple = SimpleModel.objects.create()
        obj = filler.create()[0]
        self.assertEqual(obj.o2o, simple)

        self.assertRaises(CreateInstanceError, filler.create)

    def test_generate_fk_for_o2o(self):
        # OneToOneField is the same as a ForeignKey with unique=True
        filler = AutoFixture(O2OModel, generate_fk=True)

        all_o2o = set()
        for obj in filler.create(10):
            all_o2o.add(obj.o2o)

        self.assertEqual(set(SimpleModel.objects.all()), all_o2o)

    def test_follow_m2m(self):
        related = AutoFixture(SimpleModel).create()[0]
        self.assertEqual(SimpleModel.objects.count(), 1)

        filler = AutoFixture(
            M2MModel,
            follow_m2m=(2, 10))
        for obj in filler.create(10):
            self.assertEqual(list(obj.m2m.all()), [related])

    def test_follow_only_some_m2m(self):
        related = AutoFixture(SimpleModel).create()[0]
        self.assertEqual(SimpleModel.objects.count(), 1)
        other_related = AutoFixture(OtherSimpleModel).create()[0]
        self.assertEqual(OtherSimpleModel.objects.count(), 1)

        filler = AutoFixture(
            M2MModel,
            none_p=0,
            follow_m2m={
                'm2m': (2, 10),
            })
        for obj in filler.create(10):
            self.assertEqual(list(obj.m2m.all()), [related])
            self.assertEqual(list(obj.secondm2m.all()), [])

    def test_generate_m2m(self):
        filler = AutoFixture(
            M2MModel,
            none_p=0,
            generate_m2m=(1, 5))
        all_m2m = set()
        all_secondm2m = set()
        for obj in filler.create(10):
            self.assertTrue(1 <= obj.m2m.count() <= 5)
            self.assertTrue(1 <= obj.secondm2m.count() <= 5)
            all_m2m.update(obj.m2m.all())
            all_secondm2m.update(obj.secondm2m.all())
        self.assertEqual(SimpleModel.objects.count(), len(all_m2m))
        self.assertEqual(OtherSimpleModel.objects.count(), len(all_secondm2m))

    def test_generate_only_some_m2m(self):
        filler = AutoFixture(
            M2MModel,
            none_p=0,
            generate_m2m={
                'm2m': (1, 5),
            })
        all_m2m = set()
        all_secondm2m = set()
        for obj in filler.create(10):
            self.assertTrue(1 <= obj.m2m.count() <= 5)
            self.assertEqual(0, obj.secondm2m.count())
            all_m2m.update(obj.m2m.all())
            all_secondm2m.update(obj.secondm2m.all())
        self.assertEqual(SimpleModel.objects.count(), len(all_m2m))
        self.assertEqual(OtherSimpleModel.objects.count(), len(all_secondm2m))

    def test_generate_m2m_with_intermediary_model(self):
        filler = AutoFixture(
            M2MModelThrough,
            generate_m2m=(1, 5))
        all_m2m = set()
        for obj in filler.create(10):
            self.assertTrue(1 <= obj.m2m.count() <= 5)
            all_m2m.update(obj.m2m.all())
        self.assertEqual(SimpleModel.objects.count(), len(all_m2m))

    def test_generate_fk_to_self(self):
        ''' When a model with a reference to itself is encountered, If NULL is allowed
            don't generate a new instance of itself as a foreign key, so as not to reach
            pythons recursion limit
        '''
        filler = AutoFixture(SelfReferencingModel, generate_fk=True)
        model = filler.create_one()
        self.assertEqual(model.parent_self, None)
        self.assertEqual(SelfReferencingModel.objects.count(), 1)

    def test_generate_fk_to_self_no_null(self):
        ''' Throw an exception when a model is encountered which references itself but
            does not allow NULL values to be set.
        '''
        filler = AutoFixture(SelfReferencingModelNoNull, generate_fk=True)
        self.assertRaises(CreateInstanceError, filler.create_one)

    def test_generate_fk_to_self_follow(self):
        filler = AutoFixture(SelfReferencingModel, follow_fk=True)
        first = filler.create_one()
        self.assertEqual(SelfReferencingModel.objects.count(), 1)

        filler = AutoFixture(SelfReferencingModel, follow_fk=True)
        second = filler.create_one()
        self.assertEqual(SelfReferencingModel.objects.count(), 2)
        self.assertEqual(second.parent_self, first)


class TestInheritModel(TestCase):
    def test_inheritence_model(self):
        filler = AutoFixture(InheritModel)
        filler.create(10)
        self.assertEqual(InheritModel.objects.count(), 10)

    def test_inheritence_unique_together_model(self):
        filler = AutoFixture(InheritUniqueTogetherModel)
        filler.create(10)
        self.assertEqual(InheritUniqueTogetherModel.objects.count(), 10)


class TestUniqueConstraints(TestCase):
    def test_unique_field(self):
        filler = AutoFixture(UniqueTestModel)
        count = len(filler.model._meta.
            get_field_by_name('choice1')[0].choices)
        for obj in filler.create(count):
            pass

    def test_unique_together(self):
        filler = AutoFixture(UniqueTogetherTestModel)
        count1 = len(filler.model._meta.
            get_field_by_name('choice1')[0].choices)
        count2 = len(filler.model._meta.
            get_field_by_name('choice2')[0].choices)
        for obj in filler.create(count1 * count2):
            pass


class TestGenerators(TestCase):
    def test_instance_selector(self):
        AutoFixture(SimpleModel).create(10)

        result = generators.InstanceSelector(SimpleModel).generate()
        self.assertEqual(result.__class__, SimpleModel)

        for i in range(10):
            result = generators.InstanceSelector(
                SimpleModel, max_count=10).generate()
            self.assertTrue(0 <= len(result) <= 10)
            for obj in result:
                self.assertEqual(obj.__class__, SimpleModel)
        for i in range(10):
            result = generators.InstanceSelector(
                SimpleModel, min_count=5, max_count=10).generate()
            self.assertTrue(5 <= len(result) <= 10)
            for obj in result:
                self.assertEqual(obj.__class__, SimpleModel)
        for i in range(10):
            result = generators.InstanceSelector(
                SimpleModel, min_count=20, max_count=100).generate()
            # cannot return more instances than available
            self.assertEqual(len(result), 10)
            for obj in result:
                self.assertEqual(obj.__class__, SimpleModel)

        # works also with queryset as argument
        result = generators.InstanceSelector(SimpleModel.objects.all()).generate()
        self.assertEqual(result.__class__, SimpleModel)


class TestLinkClass(TestCase):
    def test_flat_link(self):
        link = Link(('foo', 'bar'))
        self.assertTrue('foo' in link)
        self.assertTrue('bar' in link)
        self.assertFalse('spam' in link)

        self.assertEqual(link['foo'], None)
        self.assertEqual(link['spam'], None)

    def test_nested_links(self):
        link = Link(('foo', 'foo__bar', 'spam__ALL'))
        self.assertTrue('foo' in link)
        self.assertFalse('spam' in link)
        self.assertFalse('egg' in link)

        foolink = link.get_deep_links('foo')
        self.assertTrue('bar' in foolink)
        self.assertFalse('egg' in foolink)

        spamlink = link.get_deep_links('spam')
        self.assertTrue('bar' in spamlink)
        self.assertTrue('egg' in spamlink)

    def test_links_with_value(self):
        link = Link({'foo': 1, 'spam__egg': 2}, default=0)
        self.assertTrue('foo' in link)
        self.assertEqual(link['foo'], 1)
        self.assertFalse('spam' in link)
        self.assertEqual(link['spam'], 0)

        spamlink = link.get_deep_links('spam')
        self.assertTrue('egg' in spamlink)
        self.assertEqual(spamlink['bar'], 0)
        self.assertEqual(spamlink['egg'], 2)

    def test_always_true_link(self):
        link = Link(True)
        self.assertTrue('field' in link)
        self.assertTrue('any' in link)

        link = link.get_deep_links('field')
        self.assertTrue('field' in link)
        self.assertTrue('any' in link)

        link = Link(('ALL',))
        self.assertTrue('field' in link)
        self.assertTrue('any' in link)

        link = link.get_deep_links('field')
        self.assertTrue('field' in link)
        self.assertTrue('any' in link)

    def test_inherit_always_true_value(self):
        link = Link({'ALL': 1})
        self.assertEqual(link['foo'], 1)

        sublink = link.get_deep_links('foo')
        self.assertEqual(sublink['bar'], 1)


class TestRegistry(TestCase):
    def setUp(self):
        self.original_registry = autofixture.REGISTRY
        autofixture.REGISTRY = {}

    def tearDown(self):
        autofixture.REGISTRY = self.original_registry

    def test_registration(self):
        autofixture.register(SimpleModel, SimpleAutoFixture)
        self.assertTrue(SimpleModel in autofixture.REGISTRY)
        self.assertEqual(autofixture.REGISTRY[SimpleModel], SimpleAutoFixture)

    def test_create(self):
        autofixture.register(SimpleModel, SimpleAutoFixture)
        for obj in autofixture.create(SimpleModel, 10):
            self.assertEqual(obj.name, 'foo')
        obj = autofixture.create_one(SimpleModel)
        self.assertEqual(obj.name, 'foo')

    def test_overwrite_attributes(self):
        autofixture.register(SimpleModel, SimpleAutoFixture)
        for obj in autofixture.create(
                SimpleModel, 10, field_values={'name': 'bar'}):
            self.assertEqual(obj.name, 'bar')
        obj = autofixture.create_one(
            SimpleModel, field_values={'name': 'bar'})
        self.assertEqual(obj.name, 'bar')

    def test_registered_fixture_is_used_for_fk(self):
        class BasicModelFixture(AutoFixture):
            field_values={'chars': 'Hello World!'}

        autofixture.register(BasicModel, BasicModelFixture)

        fixture = AutoFixture(RelatedModel, generate_fk=['related'])
        obj = fixture.create_one()
        self.assertTrue(obj)
        self.assertEqual(obj.related.chars, 'Hello World!')

    def test_registered_fixture_is_used_for_m2m(self):
        class SimpleModelFixture(AutoFixture):
            field_values={'name': 'Jon Doe'}

        autofixture.register(SimpleModel, SimpleModelFixture)

        fixture = AutoFixture(M2MModel, generate_m2m={'m2m': (5,5)})
        obj = fixture.create_one()
        self.assertTrue(obj)

        self.assertEqual(obj.m2m.count(), 5)
        self.assertEqual(
            list(obj.m2m.values_list('name', flat=True)),
            ['Jon Doe'] * 5)


class TestAutofixtureAPI(TestCase):
    def setUp(self):
        self.original_registry = autofixture.REGISTRY
        autofixture.REGISTRY = {}

    def tearDown(self):
        autofixture.REGISTRY = self.original_registry

    def test_values_class(self):
        autofixture.register(BasicModel, BasicValueFixture)
        for obj in autofixture.create(BasicModel, 10):
            self.assertEqual(obj.chars, 'foo')
            self.assertEqual(obj.shortchars, 'a')
            self.assertEqual(obj.blankchars, 'bar')
            self.assertEqual(obj.nullchars, 'spam')
            self.assertTrue(1 <= obj.intfield <= 13)


class TestManagementCommand(TestCase):
    def setUp(self):
        from autofixture.management.commands.loadtestdata import Command
        self.command = Command()
        self.options = {
            'overwrite_defaults': None,
            'no_follow_fk': None,
            'no_follow_m2m': None,
            'generate_fk': None,
            'follow_m2m': None,
            'generate_m2m': None,
            'verbosity': '0',
            'use': '',
        }
        self.original_registry = autofixture.REGISTRY
        autofixture.REGISTRY = {}

    def tearDown(self):
        autofixture.REGISTRY = self.original_registry

    def test_basic(self):
        models = ()
        # empty attributes are allowed
        self.command.handle(*models, **self.options)
        self.assertEqual(SimpleModel.objects.count(), 0)

        models = ('autofixture_tests.SimpleModel:1',)
        self.command.handle(*models, **self.options)
        self.assertEqual(SimpleModel.objects.count(), 1)

        models = ('autofixture_tests.SimpleModel:5',)
        self.command.handle(*models, **self.options)
        self.assertEqual(SimpleModel.objects.count(), 6)

    def test_generate_fk(self):
        models = ('autofixture_tests.DeepLinkModel2:1',)
        self.options['generate_fk'] = 'related,related__related'
        self.command.handle(*models, **self.options)
        obj = DeepLinkModel2.objects.get()
        self.assertTrue(obj.related)
        self.assertTrue(obj.related.related)
        self.assertEqual(obj.related.related2, obj.related.related)

    def test_generate_fk_with_no_follow(self):
        models = ('autofixture_tests.DeepLinkModel2:1',)
        self.options['generate_fk'] = 'related,related__related'
        self.options['no_follow_fk'] = True
        self.command.handle(*models, **self.options)
        obj = DeepLinkModel2.objects.get()
        self.assertTrue(obj.related)
        self.assertTrue(obj.related.related)
        self.assertEqual(obj.related.related2, None)

    def test_generate_fk_with_ALL(self):
        models = ('autofixture_tests.DeepLinkModel2:1',)
        self.options['generate_fk'] = 'ALL'
        self.command.handle(*models, **self.options)
        obj = DeepLinkModel2.objects.get()
        self.assertTrue(obj.related)
        self.assertTrue(obj.related.related)
        self.assertTrue(obj.related.related2)
        self.assertTrue(obj.related.related != obj.related.related2)

    def test_no_follow_m2m(self):
        AutoFixture(SimpleModel).create(1)

        models = ('autofixture_tests.NullableFKModel:1',)
        self.options['no_follow_m2m'] = True
        self.command.handle(*models, **self.options)
        obj = NullableFKModel.objects.get()
        self.assertEqual(obj.m2m.count(), 0)

    def test_follow_m2m(self):
        AutoFixture(SimpleModel).create(10)
        AutoFixture(OtherSimpleModel).create(10)

        models = ('autofixture_tests.M2MModel:25',)
        self.options['follow_m2m'] = 'm2m:3:3,secondm2m:0:10'
        self.command.handle(*models, **self.options)

        for obj in M2MModel.objects.all():
            self.assertEqual(obj.m2m.count(), 3)
            self.assertTrue(0 <= obj.secondm2m.count() <= 10)

    def test_generate_m2m(self):
        models = ('autofixture_tests.M2MModel:10',)
        self.options['generate_m2m'] = 'm2m:1:1,secondm2m:2:5'
        self.command.handle(*models, **self.options)

        all_m2m, all_secondm2m = set(), set()
        for obj in M2MModel.objects.all():
            self.assertEqual(obj.m2m.count(), 1)
            self.assertTrue(
                2 <= obj.secondm2m.count() <= 5 or
                obj.secondm2m.count() == 0)
            all_m2m.update(obj.m2m.all())
            all_secondm2m.update(obj.secondm2m.all())
        self.assertEqual(all_m2m, set(SimpleModel.objects.all()))
        self.assertEqual(all_secondm2m, set(OtherSimpleModel.objects.all()))

    def test_using_registry(self):
        autofixture.register(SimpleModel, SimpleAutoFixture)
        models = ('autofixture_tests.SimpleModel:10',)
        self.command.handle(*models, **self.options)
        for obj in SimpleModel.objects.all():
            self.assertEqual(obj.name, 'foo')

    def test_use_option(self):
        self.options['use'] = 'autofixture_tests.tests.SimpleAutoFixture'
        models = ('autofixture_tests.SimpleModel:10',)
        self.command.handle(*models, **self.options)
        for obj in SimpleModel.objects.all():
            self.assertEqual(obj.name, 'foo')


class TestGenericRelations(TestCase):
    def assertNotRaises(self, exc_type, func, msg=None,
            args=None, kwargs=None):
        args = args or []
        kwargs = kwargs or {}
        try:
            func(*args, **kwargs)
        except exc_type as exc:
            if msg is not None and exc.message != msg:
                return
            self.fail('{} failed with {}'.format(func, exc))

    def test_process_gr(self):
        """Tests the bug when GenericRelation field being processed
        by autofixture.base.AutoFixtureBase#process_m2m
        and through table appears as None.
        """
        count = 10
        fixture = AutoFixture(GRModel)
        self.assertNotRaises(AttributeError, fixture.create,
            msg="'NoneType' object has no attribute '_meta'", args=[count])
        self.assertEqual(GRModel.objects.count(), count)