"""
player/views.py
"""
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from djge import mixin
from world.models import Location
from mobile.models import PlayerCharacter
from player.models import Config
from player import forms

MAX_TOONS = 5


class Index(mixin.RequireUser, generic.ListView):
    model = PlayerCharacter
    template_name = 'player/index.html'
    
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['object_list'] = PlayerCharacter.objects.filter(user=self.request.user).order_by('created')
        context['cfg'] = get_object_or_404(Config, name=self.request.user)
        context['max_toons'] = MAX_TOONS
        return context


class Create(mixin.RequireUser, generic.CreateView):
    form_class = forms.CreateCharacter
    model = PlayerCharacter
    template_name = 'player/create.html'

    def get(self, request, *args, **kwargs):
        if PlayerCharacter.objects.filter(user=self.request.user).count() >= MAX_TOONS:
            messages.error(self.request, 'Already at max.', extra_tags='danger')
            return redirect('toon:index')
        return super(Create, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        if PlayerCharacter.objects.filter(user=self.request.user).count() >= MAX_TOONS:
            messages.error(self.request, 'Already at max.', extra_tags='danger')
            return super(Create, self).form_invalid(form)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.level = 1
        self.object.life = self.object.life_max = self.object.species.starting_hp
        self.object.mana = self.object.mana_max = self.object.species.starting_mp
        try:
            self.object.where = self.object.species.starting_zone
        except ValueError:
            self.object.where = get_object_or_404(Location, id=1)
        self.success_url = reverse('player:index')
        return super(Create, self).form_valid(form)


class Detail(mixin.RequireUser, mixin.RequireOwner, generic.DetailView):
    model = PlayerCharacter
    template_name = 'player/detail.html'


class Update(mixin.RequireUser, mixin.RequireOwner, generic.DetailView):
    form_class = forms.UpdateCharacter
    model = PlayerCharacter
    template_name = 'player/detail.html'


class Select(mixin.RequireUser, generic.RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        current = get_object_or_404(Config, name=self.request.user)
        current.playing_toon = get_object_or_404(PlayerCharacter, user=self.request.user, pk=self.kwargs.get('pk'))
        current.save()
        self.url = reverse('index')
        return super(Select, self).get_redirect_url(*args, **kwargs)
