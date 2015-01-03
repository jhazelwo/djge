"""
djge/urls.py
"""
from djgesettings import LOCAL_ADMIN_URL

from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
                       url(r'^install/$', views.InstallView.as_view(), name='install'),
                       url(r'^$', views.Triage.as_view(), name='index'),
                       #
                       url(r'^player/', include('player.urls', namespace='player')),
                       url(r'^encounter/', include('encounter.urls', namespace='encounter')),
                       url(r'^world/', include('world.urls', namespace='world')),
                       #
                       url(r'^auth/', TemplateView.as_view(template_name='base.html'), name='auth'),
                       url(LOCAL_ADMIN_URL, include(admin.site.urls)),
                       )
