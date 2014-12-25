"""
world/urls.py
"""
from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
     url(r'^(?P<pk>\d+)/$', views.Detail.as_view(), name='detail'),
)
