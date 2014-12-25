"""
player/models.py
"""
from django.db import models
from django.contrib.auth.models import User

from djge.models import UltraModel

from mobile.models import PlayerCharacter


class Config(UltraModel):
    name = models.ForeignKey(User, unique=True)
    playing_toon = models.ForeignKey(PlayerCharacter, null=True, blank=True)
    CHOICE = (
        ('29',  'Unplayable'),
        ('90',  'Normal'),
        ('120', 'CompleteCookie'),
    )
    fov = models.CharField(max_length=3, choices=CHOICE, default=CHOICE[1][0])
