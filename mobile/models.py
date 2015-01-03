"""
mobile/models.py

Category:
    A type of Mobile

BaseMobile:
    Inherited by PlayerCharacter and NonPlayerCharacter

PlayerCharacter:
    A character (mobile) controlled/owned by a person

NonPlayerCharacter:
    Template objects for mobiles controlled by the program during encounters

"""
import time
import random

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from djge.models import UltraModel
from world.models import Location
from inventory.models import Item, Container


class Category(UltraModel):
    """
    A species/race/type of Mobile. Things like Dragon, Elf, Stationwagon, Fighter Jet, etc...

    If playable then 'spawn' will be where new PlayerCharacters will be placed on creation.
    else spawn is the world.Location where the NPC will spawn during /encounter/s.
    """
    name = models.CharField(max_length=64)
    playable = models.BooleanField(default=False)
    spawn = models.ForeignKey(Location, null=True, blank=True, related_name='basemobiletype')
    life_max = models.PositiveSmallIntegerField(default=1)  # Values from 0 to 32767
    # energy_max = models.IntegerField(default=0)


class BaseMobile(UltraModel):
    """
    PC and NPC classes inherit this.
    Put all attirbutes common to mobiles here except
        category-specific traits such as spawn
        location and starting life.
    """
    name = models.CharField(max_length=64)
    level = models.IntegerField(default=1)
    #
    life = models.IntegerField(default=1)
    life_max = models.IntegerField(default=1)
    #
    category = models.ForeignKey('Category', null=True)
    #
    base_offense = models.IntegerField(default=1)
    #
    base_defense = models.IntegerField(default=1)
    #
    funk = models.IntegerField(default=100)
    CHOICES = (
        ('nonenone', ''),
        ('xtradodg', ''),
        ('dbledamg', ''),
        ('funkregn', ''),
        ('magiheal', ''),
        ('hitsteal', ''),
        ('dbleatta', ''),
        ('dbleheal', ''),
    )
    c01 = models.CharField(max_length=8, choices=CHOICES, default=CHOICES[0][0])
    c02 = models.CharField(max_length=8, choices=CHOICES, default=CHOICES[0][0])
    c03 = models.CharField(max_length=8, choices=CHOICES, default=CHOICES[0][0])
    c04 = models.CharField(max_length=8, choices=CHOICES, default=CHOICES[0][0])
    c05 = models.CharField(max_length=8, choices=CHOICES, default=CHOICES[0][0])
    c06 = models.CharField(max_length=8, choices=CHOICES, default=CHOICES[0][0])
    c07 = models.CharField(max_length=8, choices=CHOICES, default=CHOICES[0][0])
    c08 = models.CharField(max_length=8, choices=CHOICES, default=CHOICES[0][0])

    def funkup(self, amount=None):
        if amount is not None:
            # If amount is overridden then just add it without checking
            self.funk += amount
        else:
            amount = 2
            if self.autoact('funkregn'):
                self.bark('AUTO: bonus Funk regen')
                amount = 20  # cost of self.autoact + 10
            self.funk += amount
        #
        if self.funk > 100:
            self.funk = 100
        self.save()

    def lifeup(self, percent=1):
        total = int(self.life_max)
        heal = int(total * (percent / 100.0)) + 1
        self.life += heal
        if self.life > total:
            self.life = total
        self.save()

    def autoact(self, check):
        if self.funk < 10:
            return False
        chance = 0
        for this in [self.c01, self.c02, self.c03, self.c04, self.c05, self.c06, self.c07, self.c08]:
            if this == check:
                chance += 1
        if chance > 0:
            i = random.randint(1, 10)
            if i <= chance:
                self.funk -= 10
                if self.funk < 0:
                    self.funk = 0
                self.save()
                # print('Funk {0} succceeded with roll of {1} being lower than {2}'.format(check, i, chance))
                return True
        return False

    def is_dead(self):
        if self.life <= 0:
            return True
        return False

    class Meta:
        abstract = True


class PlayerCharacter(BaseMobile):
    """
    A mobile controlled by a player (real person)
    """
    user = models.ForeignKey(User)
    where = models.ForeignKey(Location)
    equip_offense = models.ForeignKey(Item, null=True, blank=True, related_name='pceqoff')
    equip_defense = models.ForeignKey(Item, null=True, blank=True, related_name='pceqdef')
    storage = models.ForeignKey(Container, null=True, blank=True)

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
        # self.journal_set.append(event)
        if event is not None:
            print('{0} {1}'.format(time.strftime('%Y%m%d.%H%M%S+UTC', time.gmtime()), event))
            return True
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


class NonPlayerCharacter(BaseMobile):
    """
    Your static/global inventory of NPCs, monsters, vendors, kings, spaceships, whatever.

    Use classes in /encounter/ to instantiate NPC objects here.
    """
    CHOICE = (
        ('10',  'Friendly'),
        ('20',  'Neutral'),
        ('30',  'Hostile'),
        ('40',  'Invulnerable'),
    )
    attitude = models.CharField(max_length=2, choices=CHOICE, default=CHOICE[0][0])
    spawn_chance = models.IntegerField(default=100,
                                       validators=[
                                           MinValueValidator(1),
                                           MaxValueValidator(100)
                                       ])
    spawn_count = models.IntegerField(default=1)
    # xp = ...
    # $$ = ...
    # parts = ...
