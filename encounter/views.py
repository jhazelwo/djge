"""
encounter/views.py
"""
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from djge import mixin
from world.models import Location
from mobile.models import PlayerCharacter, NonPlayerCharacter
from player.models import Config
from encounter.models import Battle


class Attack(mixin.RequireUser, mixin.RequireOwner, generic.DetailView):
    model = Battle

    def get(self, request, *args, **kwargs):
        target = get_object_or_404(NonPlayerCharacter, id=kwargs.get('targetpk'))
        user_is = get_object_or_404(Config, name=self.request.user)
        character_is = user_is.playing_toon
        the_fight = character_is.in_combat()
        #
        if target not in the_fight.npcs.all():
            raise Http404
        #
        target.life -= 100
        target.save()
        if target.life <= 0:
            messages.success(self.request, 'opponent defeated')
            target.delete()
        return redirect(reverse('index'))
