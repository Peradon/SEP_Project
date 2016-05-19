from django.db import models
from enum import Enum
from django.contrib.auth.models import User

# Create your models here.


class UserModel(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True)
    department = models.CharField(max_length=50, default="None")
    position = models.CharField(max_length=50, default="None")
    phone = models.CharField(max_length=30, default="000-000-0000")

    def get_fullname(self):
        return self.user.get_full_name()

    def get_department(self):
        return self.department

    def get_position(self):
        return self.position

    def get_phone(self):
        return self.phone

    def __str__(self):
        return self.user.get_full_name()

class TodoList(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="todolist")
    taskDescription = models.TextField('taskDescription', max_length=1000, null=False)

    def get_description(self):
        return self.taskDescription

class MeetingRoom(models.Model):
    roomName = models.CharField(max_length=50, primary_key=True)

    def get_room(self):
        return self.roomName

    def __str__(self):
        return self.roomName

class Reservation(models.Model):
    topic = models.CharField(max_length=50)
    start = models.DateTimeField()
    end = models.DateTimeField()
    room = models.ForeignKey(MeetingRoom)
    owner = models.ForeignKey(UserModel, default=0)

    def get_topic(self):
        return self.topic

    def get_time(self):
        return str(self.start) + " - " + str(self.end)

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_room(self):
        return self.room.get_room()

    def get_owner(self):
        return self.owner.get_fullname()


class ChatRoom(models.Model):
    chatIP = models.CharField(max_length=100)
    chatPort = models.CharField(max_length=50)
    chatName = models.CharField(max_length=50)
    owner = models.ForeignKey(UserModel, default=0)

    def get_room_ip(self):
        return self.chatIP

    def get_room_port(self):
        return self.chatPort

    def get_room_name(self):
        return self.chatName

    def get_user(self):
        return self.owner


