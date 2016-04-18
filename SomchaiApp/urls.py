from django.conf.urls import url

from . import views

urlPattern = [
    url(r'^$', views.index, name='index')
]
