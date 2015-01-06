"""
world/views.py
"""
import random

from django.views import generic
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

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
        hostile_spawn = None
        try:
            hostile_spawn = NonPlayerCharacter.objects.filter(
                attitude='30'  # hostile
            ).filter(
                category=destination.basemobiletype.get()
            ).get()
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
                        if hostile_spawn.spawn_chance >= dice:
                            new_combatant = Combatant.objects.create(
                                name=hostile_spawn.name,
                                life=hostile_spawn.life_max,
                                life_max=hostile_spawn.life_max,
                                funk=100,
                                user=self.request.user)
                            newfight.npcs.add(new_combatant)
                    character.bark('Attacked by {0} {1}s!'.format(newfight.npcs.count(), hostile_spawn))
            #
        return super(Move, self).get_redirect_url(*args, **kwargs)
