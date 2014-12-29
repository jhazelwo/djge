"""
player/view/triage.py
"""
from django.views import generic
from django.contrib import messages
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
        self.template_name = 'player/move.html'
        #
        user_is = self.request.user.config_set.get()
        if not user_is.playing_toon:
            return redirect(reverse('player:index'))
        character_is = user_is.playing_toon
        #
        if character_is.in_combat():
            context['fight'] = self.request.user.battle_set.get()
            self.template_name = 'encounter/battle.html'
        #
        context['character'] = character_is
        return self.render_to_response(context)