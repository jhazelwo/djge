"""
player/models.py
"""

from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from mobile.models import BaseMobile
from djge.models import UltraModel
from world.models import Location
from inventory.models import Item, Container


class Journal(UltraModel):
    """

    """
    name = models.ForeignKey('PlayerCharacter')

    class Meta:
        ordering = ['-created']


class PlayerCharacter(BaseMobile):
    """
    A mobile controlled by a player (real person)
    """
    user = models.ForeignKey(User)
    where = models.ForeignKey(Location)
    #
    equip_offense01 = models.ForeignKey(Item, blank=True, null=True, related_name='bmeo01')
    #
    equip_defense01 = models.ForeignKey(Item, blank=True, null=True, related_name='bmed01')
    equip_defense02 = models.ForeignKey(Item, blank=True, null=True, related_name='bmed02')
    #

    class Meta:
        unique_together = (('name', 'user'),)

    def get_absolute_url(self):
        return reverse('player:detail', kwargs={'pk': self.pk})

    def relocate(self, destination):
        if self.in_combat():
            return False
        if destination not in self.where.link.all():
            return False
        self.where = destination
        self.save()
        return True

    def in_combat(self):
        try:
            this = self.battle_set.get()
        except ObjectDoesNotExist:
            return False
        if this.npcs.count() == 0:
            this.delete()
            return False
        return this

    def bark(self, event=None):
        """
        Update self's journal with 'event'
        """
        if event is not None:
            try:
                Journal.objects.create(
                    name=self,
                    notes=event
                )
                return True
            except Exception as e:
                print('{0} {1}'.format(time.strftime('%Y%m%d.%H%M%S+UTC', time.gmtime()), event))
                print('{0} {1}'.format(time.strftime('%Y%m%d.%H%M%S+UTC', time.gmtime()), e))
        return False

    def on_death(self):
        """
        Do custom stuff when a Player's Character dies.
        """
        self.bark('I was killed.')
        self.where = self.category.spawn
        self.life = self.life_max
        for this in self.battle_set.get().npcs.all():
            this.delete()
        # self.cool -= 9001
        self.save()
        return True

    def heal_self(self):
        diff = self.life_max - self.life
        self.life = self.life_max
        self.save()
        return diff


class Config(UltraModel):
    """

    """
    name = models.ForeignKey(User, unique=True)
    playing_toon = models.ForeignKey('PlayerCharacter', null=True, blank=True)
    auto_loot = models.BooleanField(default=True)
    #
    # Account-wide storage
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
