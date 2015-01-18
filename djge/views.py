"""
djge/views.py
"""
from django.contrib.auth.models import User
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse, reverse_lazy

from djge import mixin
from player.models import Config
from world.models import Location
from world.models import Category as LocationCatagory
from mobile.models import Category as MobileCategory
# from mobile.models import NonPlayerCharacter
from inventory.models import BaseItem


class LogOut(generic.RedirectView):
    """ Blindly log out any request that hits this url with a GET """
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(self.request, 'You have logged out!')
        return super(LogOut, self).get(request, *args, **kwargs)


class Triage(mixin.RequireUser, generic.TemplateView):
    """
    Default / view, show data based on character's state.
    """
    template_name = 'impossibru/404.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        self.template_name = 'world/move.html'
        #
        account, created = Config.objects.get_or_create(name=self.request.user)
        if not account.playing_toon:
            return redirect(reverse('player:index'))
        character = account.playing_toon
        context['journal'] = character.journal_set.all()[:16]
        #
        if character.in_combat():
            self.template_name = 'encounter/battle.html'
        #
        context['character'] = character
        # messages.info(self.request, 'info')
        # messages.success(self.request, 'success')
        # messages.error(self.request, 'error')
        # messages.warning(self.request, 'warning')
        return self.render_to_response(context)


class InstallView(mixin.RequireUser, generic.TemplateView):
    """
    Create some very basic initial data to make it a bit
    easier to start building your game world.
    """
    template_name = 'install.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #
        if BaseItem.objects.count() == 0:
            this = BaseItem.objects.create(
                name='a base item',
                quality='70',   # 'Legendary'
                category='30',  # 'offense'
            )
            messages.success(self.request, 'Made {0}'.format(this))
        #
        if LocationCatagory.objects.count() == 0:
            this = LocationCatagory.objects.create(
                name='safe',
                notes='safe location',
            )
            messages.success(self.request, 'Made {0}'.format(this))
        #
        if Location.objects.count() == 0:
            this = Location.objects.create(
                name='Quntopia',
                notes='A grand city with a colossal monument to The Grand Pink Flower.',
                category=LocationCatagory.objects.get(id=1),
            )
            messages.success(self.request, 'Made {0}'.format(this))
        #
        if MobileCategory.objects.count() == 0:
            this = MobileCategory.objects.create(name='mobtype')
            messages.success(self.request, 'Made {0}'.format(this))
        #
        # All registered users need to have 1 Config object for their account.
        for this in User.objects.all():
            user_is, created = Config.objects.get_or_create(name=this)
            if created:
                messages.success(self.request, 'Made config for {0}'.format(user_is))
        return self.render_to_response(context)
