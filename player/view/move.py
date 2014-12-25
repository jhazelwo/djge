"""
player/view/move.py
"""
from django.views import generic
# from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from djge import mixin
from world.models import Location
from mobile.models import PlayerCharacter, NonPlayerCharacter
from player.models import Config
from encounter.models import Battle


class Do(mixin.RequireUser, generic.RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        destination = get_object_or_404(Location, id=kwargs.get('to'))
        user_is = Config.objects.get(name=self.request.user)
        character_is = PlayerCharacter.objects.get(id=user_is.playing_toon.id)
        #
        # if Combat.objects.filter(name=character)
        # self.url = reverse('battle')
        #
        if destination in character_is.where.link.all():
            character_is.where = destination
            character_is.save()
            if character_is.where.category.random_battles:
                newfight, created = Battle.objects.ger_or_create(name=character_is)
                if created:
                    newfight.npcs.add(NonPlayerCharacter.objects.create(name='foo', attitude='30'))
        self.url = reverse('index')
        return super(Do, self).get_redirect_url(*args, **kwargs)
