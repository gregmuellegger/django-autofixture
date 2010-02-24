# -*- coding: utf-8 -*-
from django.db import models


class Post(models.Model):
    user = models.ForeignKey('auth.User',
        related_name='posts',
        null=True, blank=True)
    name = models.CharField(max_length=50)
    text = models.TextField()

    def __unicode__(self):
        return self.name
