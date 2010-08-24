# -*- coding: utf-8 -*-
import os
from datetime import datetime
from django.db import models


filepath = os.path.dirname(os.path.abspath(__file__))

def y2k():
    return datetime(2000, 1, 1)


class SimpleModel(models.Model):
    name = models.CharField(max_length=50)


class OtherSimpleModel(models.Model):
    name = models.CharField(max_length=50)


class DeepLinkModel1(models.Model):
    related = models.ForeignKey('SimpleModel')
    related2 = models.ForeignKey('SimpleModel',
        related_name='deeplinkmodel1_rel2',
        null=True, blank=True)

class DeepLinkModel2(models.Model):
    related = models.ForeignKey('DeepLinkModel1')


class NullableFKModel(models.Model):
    m2m = models.ManyToManyField('SimpleModel', null=True, blank=True)


class BasicModel(models.Model):
    chars = models.CharField(max_length=50)
    shortchars = models.CharField(max_length=2)
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
    timefield = models.TimeField()

    decimalfield = models.DecimalField(max_digits=10, decimal_places=4)

    emailfield = models.EmailField()
    ipaddressfield = models.IPAddressField()
    urlfield = models.URLField()
    rfilepathfield = models.FilePathField(path=filepath, recursive=True)
    filepathfield = models.FilePathField(path=filepath)
    mfilepathfield = models.FilePathField(path=filepath, match=r'^.+\.py$')


class UniqueTestModel(models.Model):
    CHOICES = [(i,i) for i in range(10)]

    choice1 = models.PositiveIntegerField(choices=CHOICES, unique=True)


class UniqueTogetherTestModel(models.Model):
    CHOICES = [(i,i) for i in range(10)]

    choice1 = models.PositiveIntegerField(choices=CHOICES)
    choice2 = models.PositiveIntegerField(choices=CHOICES)

    class Meta:
        unique_together = ('choice1', 'choice2')


class RelatedModel(models.Model):
    related = models.ForeignKey(BasicModel, related_name='rel1')
    limitedfk = models.ForeignKey(SimpleModel,
        limit_choices_to={'name__exact': 'foo'}, related_name='rel2',
        null=True, blank=True)


class O2OModel(models.Model):
    o2o = models.OneToOneField(SimpleModel)


class M2MModel(models.Model):
    m2m = models.ManyToManyField(SimpleModel, related_name='m2m_rel1')
    secondm2m = models.ManyToManyField(OtherSimpleModel, related_name='m2m_rel2',
        null=True, blank=True)

class ThroughModel(models.Model):
    simple = models.ForeignKey('SimpleModel')
    other = models.ForeignKey('M2MModelThrough')

class M2MModelThrough(models.Model):
    m2m = models.ManyToManyField(SimpleModel, related_name='m2mthrough_rel1',
        through=ThroughModel)
