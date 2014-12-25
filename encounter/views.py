"""
encounter/views.py
"""
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from djge import mixin
from world.models import Location
from mobile.models import PlayerCharacter, NonPlayerCharacter
from player.models import Config
from encounter.models import Battle


class Attack(mixin.RequireUser, generic.RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        messages.info(self.request, 'encounter/views.py:Attack')
        self.url = reverse('index')
        return super(Attack, self).get_redirect_url(*args, **kwargs)
