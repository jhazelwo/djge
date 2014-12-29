"""
encounter/urls.py
"""
from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
                       url(r'^battle/(?P<pk>\d+)/attack/(?P<targetpk>\d+)$', views.Attack.as_view(), name='attack'),
                       url(r'^battle/(?P<pk>\d+)/healself$', views.HealSelf.as_view(), name='healself'),
                       )
