"""
player/models.py
"""
from django.db import models
from django.contrib.auth.models import User

from djge.models import UltraModel

from mobile.models import PlayerCharacter
from inventory.models import Container


class Config(UltraModel):
    name = models.ForeignKey(User, unique=True)
    playing_toon = models.ForeignKey(PlayerCharacter, null=True, blank=True)
    storage = models.ForeignKey(Container, null=True, blank=True)
    CHOICE = (
        ('29',  'Unplayable'),
        ('90',  'Normal'),
        ('120', 'CompleteCookie'),
    )
    fov = models.CharField(max_length=3, choices=CHOICE, default=CHOICE[1][0])
    CHOICES = (
        ('29', 'TV'),
        ('30', 'Console'),
        ('60', 'PC'),
    )
    fps = models.CharField(max_length=3, choices=CHOICES, default=CHOICES[0][0])

"""
class Journal(UltraModel):
    name = models.ForeignKey(PlayerCharacter)
    user = models.ForeignKey(User)

    def append(self, event):
        pass
"""
