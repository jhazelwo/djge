"""
encounter/models.py
"""
import time

from django.db import models
from django.contrib.auth.models import User

from djge.models import UltraModel
from mobile.models import BaseMobile
from player.models import PlayerCharacter


class Combatant(BaseMobile):
    user = models.ForeignKey(User)

    def bark(self, event=None):
        """
        NPC's journal is the floor
        """
        if event is not None:
            print('{0} {1}'.format(time.strftime('%Y%m%d.%H%M%S+UTC', time.gmtime()), event))
            return True
        return False

    def on_death(self):
        """
        Execute this code when this NPC dies.
        """
        # self.bark('{0} was killed'.format(self))
        return self.delete()


class Battle(UltraModel):
    name = models.ForeignKey(PlayerCharacter, unique=True)
    user = models.ForeignKey(User)
    npcs = models.ManyToManyField('Combatant')
    # log = ...

    def delete(self, using=None):
        for this in self.npcs.all():
            this.delete()
        return super(Battle, self).delete()

    def attack(self, attacker, target):
        if target.autoact('xtradodg'):
            target.bark('AUTO: Dodged attack from {0}'.format(attacker))
            attacker.bark('Missed {0}!'.format(target))
            return False
        #
        try:
            equipped_damage = attacker.equip_offense.base.power
        except AttributeError:
            equipped_damage = 0
        #
        total_damage = attacker.base_offense + equipped_damage
        if attacker.autoact('dbledamg'):
            total_damage *= 2
            target.bark('AUTO: Doing double damage to {0}'.format(target))
        target.life -= total_damage
        attacker.bark('Did {0} damage to {1}'.format(total_damage, target))
        target.bark('Took {0} damage from {1}'.format(total_damage, attacker))
        target.save()
        if target.is_dead():
            target.on_death()
        #
        return total_damage
