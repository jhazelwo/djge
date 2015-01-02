"""
player/view/move.py
"""
import random

from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from djge import mixin
from world.models import Location, Category
from mobile.models import PlayerCharacter, NonPlayerCharacter
from mobile.models import Category as NonPlayerCharacterCategory
from player.models import Config
from encounter.models import Battle, Combatant


class Do(mixin.RequireUser, generic.RedirectView):
    permanent = False
    query_string = False
    url = reverse_lazy('index')

    def get_redirect_url(self, *args, **kwargs):
        destination = get_object_or_404(Location, id=kwargs.get('id'))
        character = self.request.user.config_set.get().playing_toon
        hostile_spawn = None
        try:
            hostile_spawn = NonPlayerCharacter.objects.filter(
                attitude='30'  # hostile
            ).filter(
                category=destination.basemobiletype.get()
            ).get()
            print(hostile_spawn)
        except ObjectDoesNotExist:
            pass
        if character.relocate(destination) is True:
            character.funkup()
            character.funkup()
            character.lifeup()
            if hostile_spawn:
                newfight, created = Battle.objects.get_or_create(name=character, user=self.request.user)
                if created:
                    for each in range(hostile_spawn.spawn_count):
                        dice = random.randint(1, 100)
                        print(dice)
                        if hostile_spawn.spawn_chance >= dice:
                            new_combatant = Combatant.objects.create(
                                name=hostile_spawn.name,
                                life=hostile_spawn.life_max,
                                life_max=hostile_spawn.life_max,
                                funk=100,
                                user=self.request.user)
                            newfight.npcs.add(new_combatant)
            #
        return super(Do, self).get_redirect_url(*args, **kwargs)
