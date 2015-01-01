"""
encounter/models.py
"""
from django.db import models
from django.contrib.auth.models import User

from djge.models import UltraModel
from mobile.models import PlayerCharacter, NonPlayerCharacter


class Combatant(UltraModel):
    name = models.ForeignKey(NonPlayerCharacter, unique=False)
    life = models.IntegerField(default=1)
    funk = models.IntegerField(default=100)
    # loot-type = ...


class Battle(UltraModel):
    name = models.ForeignKey(PlayerCharacter, unique=True)
    user = models.ForeignKey(User)
    npcs = models.ManyToManyField('Combatant')
    # log = ...
