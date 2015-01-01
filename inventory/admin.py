"""
inventory/admin.py
"""

from django.contrib import admin
from . import models

admin.site.register(models.Container)
admin.site.register(models.Attribute)
admin.site.register(models.Enchant)
admin.site.register(models.BaseItem)
admin.site.register(models.Item)
