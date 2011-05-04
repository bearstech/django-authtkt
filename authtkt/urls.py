# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from authtkt import views

urlpatterns = patterns('',
    url(r'$', views.index, name='authtkt_index'),

)
