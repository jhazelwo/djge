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
from encounter.funcs import attack, heal_self


class Attack(mixin.RequireUser, mixin.RequireOwner, generic.DetailView):
    model = Battle

    def get(self, request, *args, **kwargs):
        target = get_object_or_404(Combatant, id=kwargs.get('targetpk'))
        character = self.request.user.config_set.get().playing_toon
        the_fight = character.in_combat()
        #
        if target not in the_fight.npcs.all():
            raise Http404
        #
        damage_done = attack(self, character, target)
        if damage_done:
            messages.success(self.request, 'Did {0} damage to {1}'.format(damage_done, target))
        else:
            messages.warning(self.request, '{0} evaded attack!'.format(target))
        if target.life <= 0:
            messages.success(self.request, '{0} defeated'.format(target))
            target.delete()
        #
        for this_npc in the_fight.npcs.all():
            damage_recv = attack(self, this_npc, character)
            if damage_recv is not False:
                messages.error(self.request,
                               'Took {0} damage from {1}'.format(damage_recv, this_npc),
                               extra_tags='danger')
            else:
                messages.success(self.request, '{0} evaded attack!'.format(character))
            this_npc.funkup()
        #
        if character.autoact('funkregn'):
            character.funkup(10 + 10)  # initial funk cost + bonus
        else:
            character.funkup()
        #
        return redirect(reverse('index'))


class HealSelf(mixin.RequireUser, mixin.RequireOwner, generic.DetailView):
    model = Battle

    def get(self, request, *args, **kwargs):
        account = self.request.user.config_set.get()
        character = account.playing_toon
        the_fight = character.in_combat()
        #
        res = heal_self(character)
        messages.success(self.request, 'Restored {0} life.'.format(res))
        for this_npc in the_fight.npcs.all():
            damage_recv = attack(self, this_npc, character)
            if damage_recv is not False:
                messages.error(self.request,
                               'Took {0} damage from {1}'.format(damage_recv, this_npc),
                               extra_tags='danger')
            else:
                messages.warning(self.request, '{0} missed!'.format(this_npc))
        character.funkup()
        for this_npc in the_fight.npcs.all():
            this_npc.funkup()
        return redirect(reverse('index'))
