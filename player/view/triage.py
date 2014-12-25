"""
player/view/triage.py
"""
from django.views import generic
# from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy, reverse

from djge import mixin
from mobile.models import PlayerCharacter
from player.models import Config
from encounter.models import Battle


class Do(mixin.RequireUser, generic.TemplateView):
    template_name = 'impossibru/404.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #
        user_is, created = Config.objects.get_or_create(name=self.request.user)
        if not user_is.playing_toon:
            return redirect(reverse('player:index'))
        character_is = PlayerCharacter.objects.get(id=user_is.playing_toon.id)
        #
        unresolved_combat = Battle.objects.filter(name=user_is.playing_toon)
        if unresolved_combat.count() > 0:
            context['fight'] = unresolved_combat
            self.template_name = 'encounter/battle.html'
        else:
            context['location'] = character_is.where
            self.template_name = 'player/move.html'
        #
        context['playing_toon'] = user_is.playing_toon
        return self.render_to_response(context)
