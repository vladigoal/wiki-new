# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from views import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    ('^$', auth_check),
    (r'index.html', manual_view),
    #(r'^manual/', include('manual.urls')),
    #(r'^cabinet/', include('cabinet.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS[0]}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
