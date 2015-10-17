# -*- coding: utf-8 -*-
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import utc

from autofixture.compat import get_GenericForeignKey
from autofixture.compat import get_GenericRelation

try:
    from django.db.models import GenericIPAddressField as IPAddressField
except ImportError:
    from django.models import IPAddressField

filepath = os.path.dirname(os.path.abspath(__file__))


def y2k():
    return datetime(2000, 1, 1).replace(tzinfo=utc)


class SimpleModel(models.Model):
    name = models.CharField(max_length=50)


class OtherSimpleModel(models.Model):
    name = models.CharField(max_length=50)


class UniqueNullFieldModel(models.Model):
    name = models.CharField(max_length=15, null=True, blank=True, unique=True)


class UniqueTogetherNullFieldModel(models.Model):
    field_one = models.CharField(max_length=15, null=True, blank=True)
    field_two = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        unique_together = ['field_one', 'field_two']


class MultipleUniqueTogetherNullFieldModel(models.Model):
    field_one = models.CharField(max_length=15, null=True, blank=True)
    field_two = models.CharField(max_length=15, null=True, blank=True)

    field_three = models.CharField(max_length=15, null=True, blank=True)
    field_four = models.CharField(max_length=15, null=True, blank=True)
    field_five = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        verbose_name = 'Multi unique_together null field'
        unique_together = (
            ['field_one', 'field_two'],
            ['field_three', 'field_four', 'field_five'],
        )


class DeepLinkModel1(models.Model):
    related = models.ForeignKey('SimpleModel')
    related2 = models.ForeignKey('SimpleModel',
                                 related_name='deeplinkmodel1_rel2',
                                 null=True,
                                 blank=True)


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
    blankfloatfield = models.FloatField(null=True, blank=True)
    floatfield = models.FloatField()

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
    ipaddressfield = IPAddressField()
    urlfield = models.URLField()
    rfilepathfield = models.FilePathField(path=filepath, recursive=True)
    filepathfield = models.FilePathField(path=filepath)
    mfilepathfield = models.FilePathField(path=filepath, match=r'^.+\.py$')
    imgfield = models.ImageField(upload_to='_autofixtures')


class UniqueTestModel(models.Model):
    CHOICES = [(i, i) for i in range(10)]

    choice1 = models.PositiveIntegerField(choices=CHOICES, unique=True)


class UniqueTogetherTestModel(models.Model):
    CHOICES = [(i, i) for i in range(10)]

    choice1 = models.PositiveIntegerField(choices=CHOICES)
    choice2 = models.PositiveIntegerField(choices=CHOICES)

    class Meta:
        unique_together = ('choice1', 'choice2')


class RelatedModel(models.Model):
    related = models.ForeignKey(BasicModel, related_name='rel1')
    limitedfk = models.ForeignKey(SimpleModel,
                                  limit_choices_to={'name__exact': 'foo'},
                                  related_name='rel2',
                                  null=True,
                                  blank=True)


class O2OModel(models.Model):
    o2o = models.OneToOneField(SimpleModel)


class O2OPrimaryKeyModel(models.Model):
    o2o = models.OneToOneField(SimpleModel, primary_key=True)


class InheritModel(SimpleModel):
    extrafloatfield = models.FloatField()


class InheritUniqueTogetherModel(SimpleModel):
    extrafloatfield = models.FloatField()

    class Meta:
        unique_together = ('extrafloatfield', 'simplemodel_ptr')


class SelfReferencingModel(models.Model):
    parent_self = models.ForeignKey('self', blank=True, null=True)


class SelfReferencingModelNoNull(models.Model):
    parent_self = models.ForeignKey('self')


class M2MModel(models.Model):
    m2m = models.ManyToManyField(SimpleModel, related_name='m2m_rel1')
    secondm2m = models.ManyToManyField(
        OtherSimpleModel, related_name='m2m_rel2', null=True, blank=True)


class ThroughModel(models.Model):
    simple = models.ForeignKey('SimpleModel')
    other = models.ForeignKey('M2MModelThrough')


class M2MModelThrough(models.Model):
    m2m = models.ManyToManyField(
        SimpleModel, related_name='m2mthrough_rel1', through=ThroughModel)


class GFKModel(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = get_GenericForeignKey()('content_type', 'object_id')


class GRModel(models.Model):
    gr = get_GenericRelation()('GFKModel')


class DummyStorage(FileSystemStorage):
    pass


dummy_storage = DummyStorage()


class ImageModel(models.Model):
    imgfield = models.ImageField(upload_to='_autofixtures',
                                 storage=dummy_storage)


class RelationWithCustomAutofixtureModel(models.Model):
    user = models.ForeignKey('auth.User', related_name='user1+')
    users = models.ManyToManyField('auth.User', related_name='user2+')
