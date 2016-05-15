from django.db import models
from enum import Enum
from django.contrib.auth.models import User

# Create your models here.


class UserModel(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True)
    department = models.CharField(max_length=50, default="None")
    position = models.CharField(max_length=50, default="None")

    def get_fullname(self):
        return self.user.get_full_name()

    def get_department(self):
        return self.department

    def get_position(self):
        return self.position

    def __str__(self):
        return self.user.get_full_name()

class TodoList(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="todolist")
    taskDescription = models.TextField('taskDescription', max_length=1000, null=False)

    def get_description(self):
        return self.taskDescription

class Reservation(models.Model):
    topic = models.CharField(max_length=50)
    start = models.DateTimeField()
    end = models.DateTimeField()
    room = models.CharField(max_length=50)

class ChatRoom(models.Model):
    roomIP = models.CharField(max_length=40)
    roomPort = models.CharField(max_length=10)
    roomName = models.CharField(max_length=50)

    def get_room_ip(self):
        return self.roomIP

    def get_room_port(self):
        return self.roomPort

    def get_room_name(self):
        return self.roomName

