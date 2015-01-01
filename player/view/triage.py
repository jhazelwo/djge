"""
player/view/triage.py
"""
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from djge import mixin
from player.models import Config


class Do(mixin.RequireUser, generic.TemplateView):
    template_name = 'impossibru/404.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.template_name = 'player/move.html'
        #
        account, created = Config.objects.get_or_create(name=self.request.user)
        if not account.playing_toon:
            return redirect(reverse('player:index'))
        character = account.playing_toon
        #
        if character.in_combat():
            context['fight'] = self.request.user.battle_set.filter(name=character).get()
            self.template_name = 'encounter/battle.html'
        #
        context['character'] = character
        return self.render_to_response(context)
