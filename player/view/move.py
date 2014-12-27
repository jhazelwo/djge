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
        destination = get_object_or_404(Location, id=kwargs.get('to'))
        user_is = Config.objects.get(name=self.request.user)
        character_is = PlayerCharacter.objects.get(id=user_is.playing_toon.id)
        #
        if Battle.objects.filter(name=character_is).count() == 0:
            if destination in character_is.where.link.all():
                character_is.where = destination
                character_is.save()
                if character_is.where.category.random_battles is True: # and random.randint(0, 32) <= 8:
                    newfight, created = Battle.objects.get_or_create(name=character_is, user=self.request.user)
                    if created:
                        newfight.npcs.add(NonPlayerCharacter.objects.create(name='Enemy1'))
                        newfight.npcs.add(NonPlayerCharacter.objects.create(name='Enemy2'))
        return super(Do, self).get_redirect_url(*args, **kwargs)
