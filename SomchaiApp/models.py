from django.db import models
from enum import Enum
from django.contrib.auth.models import User

# Create your models here.


class UserModel(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True)
    department = models.CharField(max_length=50, default="None")
    position = models.CharField(max_length=50, default="None")

class TodoList(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,related_name="todolist")
    taskDescription=models.TextField('taskDescription',max_length=1000,null=False)

class Reservation(models.Model):
    topic=models.CharField(max_length=50)
    start=models.DateTimeField()
    end=models.DateTimeField()
    room=models.CharField(max_length=50)
