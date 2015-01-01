"""
encounter/admin.py
"""

from django.contrib import admin
from . import models

admin.site.register(models.Battle)
admin.site.register(models.Combatant)
