"""
djge/models.py
"""
from django.db import models


class UltraModel(models.Model):
    """
    Define attributes and methods that apply to all models.

    Any models that do not inherit UltraModel do inherit models that inherit UltraModel.
    """
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)
