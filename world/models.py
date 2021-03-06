"""
world/models.py
"""
from django.db import models

from djge.models import UltraModel


class Category(UltraModel):
    name = models.CharField(max_length=64, unique=True)


class Location(UltraModel):
    name = models.CharField(max_length=64, unique=True)
    link = models.ManyToManyField('self', blank=True, null=True)
    category = models.ForeignKey('Category', blank=True, null=True)
