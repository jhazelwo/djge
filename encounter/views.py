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
from encounter.models import Battle, Combatant


class Attack(mixin.RequireUser, mixin.RequireOwner, generic.DetailView):
    model = Battle

    def get(self, request, *args, **kwargs):
        target = get_object_or_404(Combatant, id=kwargs.get('targetpk'))
        character = self.request.user.config_set.get().playing_toon
        this_fight = character.in_combat()
        if this_fight is False:
            raise Http404
        if target not in this_fight.npcs.all():
            raise Http404
        #
        this_fight.attack(character, target)
        character.bark('')
        #
        for this_npc in this_fight.npcs.all():
            this_fight.attack(this_npc, character)
            this_npc.funkup()
        #
        character.funkup()
        return redirect(reverse('index'))


class HealSelf(mixin.RequireUser, mixin.RequireOwner, generic.DetailView):
    model = Battle

    def get(self, request, *args, **kwargs):
        account = self.request.user.config_set.get()
        character = account.playing_toon
        this_fight = character.in_combat()
        #
        if this_fight is False:
            raise Http404
        #
        for this_npc in this_fight.npcs.all():
            this_fight.attack(this_npc, character)
            this_npc.funkup()
        #
        character.funkup()
        return redirect(reverse('index'))
