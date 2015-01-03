"""
world/urls.py
"""
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
                       url(r'^relocate/(?P<id>\d+)$', views.Move.as_view(), name='move'),
                       )
