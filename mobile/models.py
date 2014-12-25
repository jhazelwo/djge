"""
mobile/models.py
"""
from django.db import models
from django.contrib.auth.models import User

from djge.models import UltraModel

from world.models import Location


class Species(UltraModel):
    name = models.CharField(max_length=64)
    playable = models.BooleanField(default=False)
    starting_zone = models.ForeignKey(Location, null=True, blank=True)
    starting_hp = models.PositiveSmallIntegerField(default=1)
    starting_mp = models.PositiveSmallIntegerField(default=1)  # Values from 0 to 32767


class Gender(UltraModel):
    name = models.CharField(max_length=64)
    playable = models.BooleanField(default=False)


class BaseMobile(UltraModel):
    level = models.PositiveIntegerField(default=1)
    life = models.PositiveIntegerField(default=1)
    life_max = models.PositiveIntegerField(default=1)
    mana = models.PositiveIntegerField(default=1)
    mana_max = models.PositiveIntegerField(default=1)
    species = models.ForeignKey('Species', null=True)
    gender = models.ForeignKey('Gender', null=True)

    class Meta:
        abstract = True


class PlayerCharacter(BaseMobile):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(User)
    where = models.ForeignKey(Location)

    class Meta:
        unique_together = (('name', 'user'),)


class NonPlayerCharacter(BaseMobile):
    name = models.CharField(max_length=64)
    CHOICE = (
        ('10',  'Friendly'),
        ('20',  'Neutral'),
        ('30',  'Hostile'),
        ('40',  'Invulnerable'),
    )
    attitude = models.CharField(max_length=2, choices=CHOICE, default=CHOICE[0][1])
