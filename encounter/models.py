"""
encounter/models.py
"""
from django.db import models
from django.contrib.auth.models import User

from mobile.models import PlayerCharacter, NonPlayerCharacter
from djge.models import UltraModel


class Battle(UltraModel):
    name = models.ForeignKey(PlayerCharacter)
    npcs = models.ManyToManyField(NonPlayerCharacter)
