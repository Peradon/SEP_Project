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
    url(r'^Todo/deleteTodo', views.deleteTodo, name='deleteTodo'),
    url(r'^Meeting/getRoom', views.getRoom, name='getRoom'),
    url(r'^Meeting/makeReserve', views.makeReserve, name='makeReserve'),
    url(r'^Meeting/getReserve', views.getReserve, name='getReserve'),
    url(r'^Meeting/deleteReserve', views.deleteReserve, name='deleteReserve'),
    url(r'^Chat/createChat', views.createChat, name='createChat'),
    url(r'^Chat/getChat', views.getChatRoom, name='getChat'),
    url(r'^Profile/getProfile', views.getProfile, name='getProfile')
]
