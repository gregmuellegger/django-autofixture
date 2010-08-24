# -*- coding: utf-8 -*-
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)


class Post(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    author = models.ForeignKey(Author)
    categories = models.ManyToManyField(Category, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.name, self.text)
