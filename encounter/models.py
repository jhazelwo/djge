"""
encounter/models.py
"""
from django.db import models
from django.contrib.auth.models import User

from djge.models import UltraModel
from mobile.models import PlayerCharacter, NonPlayerCharacter


class Battle(UltraModel):
    name = models.ForeignKey(PlayerCharacter, unique=True)
    user = models.ForeignKey(User)
    npcs = models.ManyToManyField(NonPlayerCharacter)
    # log =
