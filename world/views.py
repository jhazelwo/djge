"""
world/views.py
"""
import random

from django.views import generic
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from djge import dice
from djge import mixin
from world.models import Location
from mobile.models import NonPlayerCharacter
from encounter.models import Battle, Combatant


class Move(mixin.RequireUser, generic.RedirectView):
    permanent = False
    query_string = False
    url = reverse_lazy('index')

    def get_redirect_url(self, *args, **kwargs):
        destination = get_object_or_404(Location, id=kwargs.get('id'))
        character = self.request.user.config_set.get().playing_toon
        #
        # Find all NPC objects linked to this location by their category and are hostile.
        npcs = NonPlayerCharacter.objects.filter(attitude='30').filter(category=destination.basemobiletype.get())
        if character.relocate(destination) is True:
            character.funkup(4)
            character.lifeup()
            character.bark('Entered {0}'.format(destination))
            if npcs.count() is not 0:
                npcs = npcs.get()
                newfight, created = Battle.objects.get_or_create(name=character, user=self.request.user)
                if created:
                    for each in range(npcs.spawn_count):
                        if dice.roll(npcs.spawn_chance):
                            new_combatant = Combatant.objects.create(
                                name=npcs.name,
                                life=npcs.life_max,
                                life_max=npcs.life_max,
                                base_offense=npcs.base_offense,
                                funk=100,
                                user=self.request.user)
                            newfight.npcs.add(new_combatant)
                    if newfight.npcs.count() == 1:
                        character.bark('Attacked by a {0}!'.format(npcs))
                    elif newfight.npcs.count() > 1:
                        character.bark('Attacked by a group of {0}s!'.format(npcs))
            #
        return super(Move, self).get_redirect_url(*args, **kwargs)
