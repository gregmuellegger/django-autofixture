# -*- coding: utf-8 -*-
from decimal import Decimal
from datetime import date, datetime
from django.db import models
from django.test import TestCase
from django_testdata.autofixture import AutoFixture


def y2k():
    return datetime(2000, 1, 1)


class BasicModel(models.Model):
    chars = models.CharField(max_length=50)
    blankchars = models.CharField(max_length=100, blank=True)
    nullchars = models.CharField(max_length=100, blank=True, null=True)
    slugfield = models.SlugField()
    textfield = models.TextField()

    defaultint = models.IntegerField(default=1)
    intfield = models.IntegerField()
    pintfield = models.PositiveIntegerField()
    sintfield = models.SmallIntegerField()
    psintfield = models.PositiveSmallIntegerField()

    STRING_CHOICES = (
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
    )
    choicefield = models.CharField(choices=STRING_CHOICES, max_length=1)

    datefield = models.DateField()
    datetimefield = models.DateTimeField()
    defaultdatetime = models.DateTimeField(default=y2k)

    decimalfield = models.DecimalField(max_digits=10, decimal_places=4)

    emailfield = models.EmailField()
    bigintegerfield = models.BigIntegerField()
    ipaddressfield = models.IPAddressField()


class UniqueTestModel(models.Model):
    CHOICES = [(i,i) for i in range(10)]

    choice1 = models.PositiveIntegerField(choices=CHOICES, unique=True)


class UniqueTogetherTestModel(models.Model):
    CHOICES = [(i,i) for i in range(10)]

    choice1 = models.PositiveIntegerField(choices=CHOICES)
    choice2 = models.PositiveIntegerField(choices=CHOICES)

    class Meta:
        unique_together = ('choice1', 'choice2')


class TestBasicModel(TestCase):
    def assertEqualsOr(self, first, second, fallback):
        if first != second and not fallback:
            self.fail()

    def test_create(self):
        filler = AutoFixture(BasicModel)
        filler.create(10)
        self.assertEquals(BasicModel.objects.count(), 10)

    def test_constraints(self):
        filler = AutoFixture(
            BasicModel,
            overwrite_defaults=False)
        for obj in filler.create(100):
            self.assertTrue(len(obj.chars) > 0)
            self.assertEquals(type(obj.chars), unicode)
            self.assertTrue(type(obj.blankchars), unicode)
            self.assertEqualsOr(type(obj.nullchars), unicode, None)
            self.assertEquals(type(obj.slugfield), unicode)
            self.assertEquals(type(obj.defaultint), int)
            self.assertEquals(obj.defaultint, 1)
            self.assertEquals(type(obj.intfield), int)
            self.assertEquals(type(obj.sintfield), int)
            self.assertEquals(type(obj.pintfield), int)
            self.assertEquals(type(obj.psintfield), int)
            self.assertEquals(type(obj.datefield), date)
            self.assertEquals(type(obj.datetimefield), datetime)
            self.assertEquals(type(obj.defaultdatetime), datetime)
            self.assertEquals(obj.defaultdatetime, y2k())
            self.assertEquals(type(obj.decimalfield), Decimal)
            self.assertTrue('@' in obj.emailfield)
            self.assertTrue('.' in obj.emailfield)
            self.assertTrue(obj.ipaddressfield.count('.'), 3)
            self.assertTrue(len(obj.ipaddressfield) >= 7)


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
