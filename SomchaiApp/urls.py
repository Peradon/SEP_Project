from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login', views.authen, name='authen'),
    url(r'^logout', views.signOut, name='logout'),
    url(r'^get_session', views.get_Session, name='get session'),
    # ****
    url(r'^todo', views.todo, name='todo'),
]
