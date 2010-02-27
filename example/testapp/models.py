# -*- coding: utf-8 -*-
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    author = models.ForeignKey(Author)

    def __unicode__(self):
        return self.name
