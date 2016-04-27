from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login', views.authen, name='authen'),
    url(r'^logout', views.logout, name='logout')
]
