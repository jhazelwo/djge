"""
player/urls.py
"""
from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
                       url(r'^create-character/$', views.Create.as_view(), name='create'),
                       url(r'^(?P<pk>\d+)/$', views.Detail.as_view(), name='detail'),
                       url(r'^(?P<pk>\d+)/play/$', views.Select.as_view(), name='select'),
                       url(r'^(?P<pk>\d+)/update/$', views.Update.as_view(), name='update'),
                       url(r'^$', views.Index.as_view(), name='index'),
                       url(r'^inventory/$', views.Inventory.as_view(), name='inventory'),
                       )
