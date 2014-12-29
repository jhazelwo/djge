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
from encounter import battlestack


class Attack(mixin.RequireUser, mixin.RequireOwner, generic.DetailView):
    model = Battle

    def get(self, request, *args, **kwargs):
        target = get_object_or_404(NonPlayerCharacter, id=kwargs.get('targetpk'))
        user_is = get_object_or_404(Config, name=self.request.user)
        #
        character_is = user_is.playing_toon
        the_fight = character_is.in_combat()
        #
        if target not in the_fight.npcs.all():
            raise Http404
        #
        damage_done = battlestack.attack(self, character_is, target)
        if damage_done:
            messages.success(self.request, 'Did {0} damage to {1}'.format(damage_done, target))
        else:
            messages.warning(self.request, 'Missed {0}!'.format(target))
        if target.life <= 0:
            messages.success(self.request, '{0} defeated'.format(target))
            target.delete()
        for this_npc in the_fight.npcs.all():
            damage_recv = battlestack.attack(self, this_npc, character_is)
            if damage_recv is not False:
                messages.error(self.request,
                               'Took {0} damage from {1}'.format(damage_recv, this_npc),
                               extra_tags='danger')
            else:
                messages.warning(self.request, '{0} missed!'.format(this_npc))
        return redirect(reverse('index'))


class HealSelf(mixin.RequireUser, mixin.RequireOwner, generic.DetailView):
    model = Battle

    def get(self, request, *args, **kwargs):
        user_is = get_object_or_404(Config, name=self.request.user)
        character_is = user_is.playing_toon
        the_fight = character_is.in_combat()
        #
        res = battlestack.heal_self(character_is)
        messages.success(self.request, 'Restored {0} life.'.format(res))
        for this_npc in the_fight.npcs.all():
            damage_recv = battlestack.attack(self, this_npc, character_is)
            if damage_recv is not False:
                messages.error(self.request,
                               'Took {0} damage from {1}'.format(damage_recv, this_npc),
                               extra_tags='danger')
            else:
                messages.warning(self.request, '{0} missed!'.format(this_npc))
        return redirect(reverse('index'))
