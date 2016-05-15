from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login', views.authen, name='authen'),
    url(r'^logout', views.signOut, name='logout'),
    url(r'^get_session', views.get_Session, name='get session'),
    url(r'^get_allUser', views.get_User, name='get user'),
    # ****
    url(r'^Todo/addTodo', views.addTodo, name='addTodo'),
    url(r'^Todo/getTodo', views.getTodo, name='getTodo'),
    url(r'^Todo/deleteTodo', views.deleteTodo, name='deleteTodo')
]
