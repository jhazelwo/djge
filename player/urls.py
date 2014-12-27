"""
player/urls.py
"""
from django.conf.urls import patterns, include, url

from player.view.logout import Do as LogOut
from player.view.move import Do as Move

from player.view import character

urlpatterns = patterns('',
                       url(r'^logout/$', LogOut.as_view(), name='logout'),
                       url(r'^movemeto=(?P<to>\d+)$', Move.as_view(), name='move'),
                       #
                       #
                       url(r'^create-character/$', character.Create.as_view(), name='create'),
                       url(r'^(?P<pk>\d+)/$', character.Detail.as_view(), name='detail'),
                       url(r'^(?P<pk>\d+)/play/$', character.Select.as_view(), name='select'),
                       url(r'^(?P<pk>\d+)/update/$', character.Update.as_view(), name='update'),
                       #
                       #
                       url(r'^$', character.Index.as_view(), name='index'),
                       )
