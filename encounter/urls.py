"""
encounter/urls.py
"""
from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
                       url(r'^battle/(?P<pk>\d+)/attack/(?P<targetpk>\d+)$', views.Attack.as_view(), name='attack'),
                       )
