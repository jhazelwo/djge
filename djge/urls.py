"""
djge/urls.py
"""
from djgesettings import LOCAL_ADMIN_URL

from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url

from player.view.triage import Do as Triage


urlpatterns = patterns('',
                       url(r'^auth/', TemplateView.as_view(template_name='base.html'), name='auth'),
                       url(r'^$', Triage.as_view(), name='index'),
                       url(r'^player/', include('player.urls', namespace='player')),
                       url(r'^encounter/', include('encounter.urls', namespace='encounter')),
                       url(LOCAL_ADMIN_URL, include(admin.site.urls)),
                       )
