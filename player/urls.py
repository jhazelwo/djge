"""
player/urls.py
"""
from django.conf.urls import patterns, include, url

from player.view.logout import Do as LogOut
from player.view.move import Do as Move

from player.view.character import Detail, Select, Create, Index

urlpatterns = patterns('',
                       url(r'^logout/$', LogOut.as_view(), name='logout'),
                       url(r'^movemeto=(?P<to>\d+)$', Move.as_view(), name='move'),
                       #
                       #
                       url(r'^create-character/$', Create.as_view(), name='create'),
                       url(r'^(?P<pk>\d+)/$', Detail.as_view(), name='detail'),
                       url(r'^(?P<pk>\d+)/play/$', Select.as_view(), name='select'),
                       #
                       #
                       url(r'^$', Index.as_view(), name='index'),
                       )
