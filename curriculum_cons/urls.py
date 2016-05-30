"""curriculum_cons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from mylates.views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('^$', index, name='home'),
    url('^register/$', register),
    url('^search/$', search),
    url('^logout/$', logout_view),
    url('^curriculum/$', curriculum),
    url('^view/(\d+)/$', view),
    url('^view/$', view),
    url('^edit/(?P<offset>[^/]+)/$', edit),
    url('^edit/(?P<offset>[^/]+)/(?P<f_id>[^/]+)/$', edit),
    url('^restore/$', send_mail),
]
