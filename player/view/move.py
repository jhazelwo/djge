"""
player/view/move.py
"""
import random

from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404

from djge import mixin
from world.models import Location
from mobile.models import PlayerCharacter, NonPlayerCharacter
from player.models import Config
from encounter.models import Battle


class Do(mixin.RequireUser, generic.RedirectView):
    permanent = False
    query_string = False
    url = reverse_lazy('index')

    def get_redirect_url(self, *args, **kwargs):
        destination = get_object_or_404(Location, id=kwargs.get('id'))
        user_is = self.request.user.config_set.get()
        character = user_is.playing_toon
        #
        if character.relocate(destination) is True:
            character.funkup()
            character.funkup()
            character.lifeup()
            #
            if character.where.category.random_battles is True:  # and random.randint(0, 32) <= 8:
                newfight, created = Battle.objects.get_or_create(name=character, user=self.request.user)
                if created:
                    newfight.npcs.add(NonPlayerCharacter.objects.create(name='Giant Rock Monster', life=2000))
                    newfight.npcs.add(NonPlayerCharacter.objects.create(name='GimP', life=100))
            #
        return super(Do, self).get_redirect_url(*args, **kwargs)
