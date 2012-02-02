from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


urlpatterns = patterns('myproject.views',

    url(r'^ajax/$', 'ajax',name='ajax'),
    url(r'^config/$', 'config',name='config'),

