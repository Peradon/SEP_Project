from django.db import models
from enum import Enum
from django.contrib.auth.models import User

# Create your models here.


class UserModel(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True)
    department = models.CharField(max_length=50, default="None")
    position = models.CharField(max_length=50, default="None")
