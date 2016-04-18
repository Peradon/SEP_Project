from django.db import models
from enum import Enum
from django.contrib.auth.models import User

# Create your models here.


class Department(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True)
    department = models.CharField(max_length=50)


class Hierarchy(models.Model):
    user = models.ForeignKey(User, unique=True, primary_key=True)
    hierarchy = models.CharField(max_length=50)


