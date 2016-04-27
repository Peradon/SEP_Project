from django.db import models
from enum import Enum
from django.contrib.auth.models import User

# Create your models here.


class UserModel(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True)
    department = models.CharField(max_length=50, default="None")
    position = models.CharField(max_length=50, default="None")

class TodoList(models.Model):
    #employee
    user=models.ForeignKey(User,unique=True,primary_key=True)
    #task description
    taskDescription = models.CharField(max_length=100)
    start=models.DateTimeField()
    end=models.DateTimeField()

class Reservation(models.Model):
    topic=models.CharField(max_length=50)
    start=models.DateTimeField()
    end=models.DateTimeField()
    room=models.CharField(max_length=50)
