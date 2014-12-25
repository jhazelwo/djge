"""
encounter/urls.py
"""
from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
                       url(r'^attackid=(?P<npcid>\d+)$', views.Attack.as_view(), name='attack'),
                       )
