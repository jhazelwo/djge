"""
djge/views.py
"""
from django.http import Http404
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from djge import mixin
from world.models import Location
from world.models import Category as LocationCatagory
from mobile.models import PlayerCharacter
from mobile.models import Category as MobileCategory
from player.models import Config


class InstallView(mixin.RequireUser, generic.TemplateView):
    template_name = 'install.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #
        try:
            this = LocationCatagory.objects.get(id=1)
        except ObjectDoesNotExist:
            this = LocationCatagory.objects.create(
                name='sanctuary',
                notes='safe location',
                random_battles=False,
            )
            messages.success(self.request, 'Made {0}'.format(this))
        #
        try:
            this = Location.objects.get(id=1)
        except ObjectDoesNotExist:
            this = Location.objects.create(
                name='Quntopia',
                notes='A grand city with a colossal monument to The Grand Pink Flower.',
                category=LocationCatagory.objects.get(id=1),
            )
            messages.success(self.request, 'Made {0}'.format(this))
        #
        try:
            this = MobileCategory.objects.get(id=1)
        except ObjectDoesNotExist:
            this = MobileCategory.objects.create(name='category')
            messages.success(self.request, 'Made {0}'.format(this))
        #
        for this in User.objects.all():
            user_is, created = Config.objects.get_or_create(name=this)
            if created:
                messages.success(self.request, 'Made config for {0}'.format(user_is))
        return self.render_to_response(context)
